#include "pss2_maps_types.hpp"

////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта M-Векторов ////////////////////////////////////////////

MapM::MapM()
{
}

MapM::MapM(int hSize, int kSize, int lSize)
{
    if (hSize <= 0 && kSize <= 0 && lSize <= 0) throw std::out_of_range("Map size value must be more than zero!");

    this->hSize = hSize;
    this->kSize = kSize;
    this->lSize = lSize;
    
    this->resize(hSize*kSize*lSize, vectorH{0, 0, 0});
}

vectorH& MapM::getVectorM(const int& h, const int& k, const int& l)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of M-vectors index value must be more or equal to zero!");

    return this->at(h * (kSize * lSize) + k * lSize + l);
}

vectorH& MapM::operator()(const int& h, const int& k, const int& l)
{
    return getVectorM(h, k, l);
}


////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта H-Векторов ////////////////////////////////////////////

MapH::MapH()
{
}

MapH::MapH(int hSize, int kSize, int lSize)
{
    if (hSize <= 0 && kSize <= 0 && lSize <= 0) throw std::out_of_range("Map size value must be more than zero!");

    this->hSize = hSize;
    this->kSize = kSize;
    this->lSize = lSize;
    
    this->resize(hSize*kSize*lSize, vectorH{0, 0, 0});
}

vectorH& MapH::getVectorH(const int& h, const int& k, const int& l)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of H-vectors index value must be more or equal to zero!");

    return this->at(h * (kSize * lSize) + k * lSize + l);
}

vectorH& MapH::operator()(const int& h, const int& k, const int& l)
{
    return getVectorH(h, k, l);
}


////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта D-расстояний //////////////////////////////////////////

MapD::MapD()
{
}

MapD::MapD(int hSize, int kSize, int lSize)
{
    if (hSize <= 0 && kSize <= 0 && lSize <= 0) throw std::out_of_range("Map size value must be more than zero!");

    this->hSize = hSize;
    this->kSize = kSize;
    this->lSize = lSize;
    
    this->resize(hSize*kSize*lSize, double{0});
}

double& MapD::getPlanDist(const int& h, const int& k, const int& l)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of D-vals index value must be more or equal to zero!");

    return this->at(h * (kSize * lSize) + k * lSize + l);
}

double& MapD::operator()(const int& h, const int& k, const int& l)
{
    return getPlanDist(h, k, l);
}



////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта F-коэффициентов ///////////////////////////////////////

MapF::MapF(){}

MapF::MapF(int hSize, int kSize, int lSize)
{
    if (hSize < 0 && kSize < 0 && lSize < 0) throw std::out_of_range("Map size value must be more than zero!");

    this->hSize = hSize;
    this->kSize = kSize;
    this->lSize = lSize;

    this->resize(hSize*kSize*lSize, complex<double>{0.0, 0.0});
}

complex<double>& MapF::getStrAmp(const int& h, const int& k, const int& l)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of F index value must be more or equal to zero!");

    const int index = h * (kSize * lSize) + k * lSize + l;
    return this->at(index);
}

complex<double>& MapF::operator()(const int& h, const int& k, const int& l)
{
    return getStrAmp(h, k, l);
}


////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта G-коэффициентов ///////////////////////////////////////

MapG::MapG() {}

MapG::~MapG()
{
    freeMap();
}

MapG::MapG(int hSize, int kSize, int lSize)
{
    if (hSize < 0 || kSize < 0 || lSize < 0) throw std::out_of_range("Map size value must be more than zero!");

    this->hSize = hSize;
    this->kSize = kSize;
    this->lSize = lSize;

    in = (fftw_complex*) fftw_malloc(hSize*kSize*lSize*sizeof(fftw_complex));
}

MapG::MapG(MapG&& other) noexcept : hSize(other.hSize), kSize(other.kSize), lSize(other.lSize), plan(other.plan), in(other.in) 
{
    other.plan = nullptr;
    other.in = nullptr;
    other.hSize = other.kSize = other.lSize = 0;
}

// Перемещающий оператор присваивания
MapG& MapG::operator=(MapG&& other) noexcept 
{
    if (this != &other) {
        // Освобождаем текущие ресурсы
        freeMap();
        
        // Перемещаем ресурсы из other
        hSize = other.hSize;
        kSize = other.kSize;
        lSize = other.lSize;
        plan = other.plan;
        in = other.in;
        
        // Обнуляем источник
        other.plan = nullptr;
        other.in = nullptr;
        other.hSize = other.kSize = other.lSize = 0;
    }
    return *this;
}

complex<double> MapG::getValG(const int& h, const int& k, const int& l)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of G index value must be more or equal to zero!");

    const double real = in[h * (kSize * lSize) + k * lSize + l][0];
    const double imag = in[h * (kSize * lSize) + k * lSize + l][1];
    return complex<double>{real, imag};
}

complex<double> MapG::operator()(const int& h, const int& k, const int& l)
{
    return getValG(h, k, l);
}

void MapG::setValG(const int& h, const int& k, const int& l, const complex<double>& val)
{
    if (h < 0 && k < 0 && l < 0) throw std::out_of_range("Map of G index value must be more or equal to zero!");

    const int index = h * (kSize * lSize) + k * lSize + l;
    in[index][0] = val.real();
    in[index][1] = val.imag();
}

void MapG::transform(MapEta& outMap)
{
    plan = fftw_plan_dft_3d(hSize, kSize, lSize, in, outMap.out, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(plan);
    fftw_destroy_plan(plan);
    plan = nullptr;
}

void MapG::freeMap()
{
    if (plan) 
    {
        fftw_destroy_plan(plan);
        plan = nullptr;
    }
    
    if (in) 
    {
        fftw_free(in);
        in = nullptr;
    }

    hSize = kSize = lSize = 0;
}


////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// Карта t-коэффициентов ///////////////////////////////////////

MapEta::MapEta(){}

MapEta::~MapEta()
{
    freeMap();
}

MapEta::MapEta(MapEta&& other) noexcept : vector<double>(std::move(other)), xSize(other.xSize), ySize(other.ySize), zSize(other.zSize), out(other.out)
{
    other.out = nullptr;
    other.xSize = other.ySize = other.zSize = 0;
}

MapEta& MapEta::operator=(MapEta&& other) noexcept
{
    if (this != &other) 
    {
        freeMap();
        
        // Перемещаем базовый класс
        static_cast<vector<double>&>(*this) = std::move(other);
        
        xSize = other.xSize;
        ySize = other.ySize;
        zSize = other.zSize;
        out = other.out;
        
        other.out = nullptr;
        other.xSize = other.ySize = other.zSize = 0;
    }
    return *this;
}

MapEta::MapEta(int xSize, int ySize, int zSize)
{
    if (xSize <= 0 && ySize <= 0 && zSize <= 0) throw std::out_of_range("Map size value must be more than zero!");

    this->xSize = xSize;
    this->ySize = ySize;
    this->zSize = zSize;

    out = (fftw_complex*) fftw_malloc(xSize*ySize*zSize*sizeof(fftw_complex));
}

complex<double> MapEta::getEta(const int& aGridIndex, const int& bGridIndex, const int& cGridIndex) const
{
    if (aGridIndex < 0 && bGridIndex < 0 && cGridIndex < 0) throw std::out_of_range("Map of Eta index value must be more or equal to zero!");

    const double real = out[aGridIndex * (ySize * zSize) + bGridIndex * zSize + cGridIndex][0];
    const double imag = out[aGridIndex * (ySize * zSize) + bGridIndex * zSize + cGridIndex][1];
    return complex<double>{real, imag};
}

void MapEta::setEta(const int& aGridIndex, const int& bGridIndex, const int& cGridIndex, const complex<double>& newVal)
{
    if (aGridIndex < 0 && bGridIndex < 0 && cGridIndex < 0) throw std::out_of_range("Map of Eta index value must be more or equal to zero!");

    const int index = aGridIndex * (ySize * zSize) + bGridIndex * zSize + cGridIndex;
    out[index][0] = newVal.real();
    out[index][1] = newVal.imag();
}

void MapEta::freeMap()
{
    if(out) 
    {
        fftw_free(out);
        out = nullptr;
    }

    this->clear();
    this->shrink_to_fit();
    xSize = ySize = zSize = 0;
}

