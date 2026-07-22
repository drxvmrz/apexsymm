#ifndef MAPS_TYPES
#define MAPS_TYPES

#include "pss2_basic_types.hpp"

// Карта H-векторов
class MapH: public vector<vectorH>
{
    public:
        // Размеры H-карты
        int hSize, kSize, lSize;

        MapH();
        MapH(int hSize, int kSize, int lSize);

        // Получает вектор по заданным индексам
        vectorH& getVectorH(const int& h, const int& k, const int& l);
        vectorH& operator()(const int& h, const int& k, const int& l);
};

// Карта M-векторов (сдвинутых H-векторов)
class MapM: public vector<vectorH>
{
    public:
        // Размеры H-карты
        int hSize, kSize, lSize;

        MapM();
        MapM(int hSize, int kSize, int lSize);

        // Получает вектор по заданным индексам
        vectorH& getVectorM(const int& h, const int& k, const int& l);
        vectorH& operator()(const int& h, const int& k, const int& l);
};

class MapD: public vector<double>
{
    public:
        int hSize, kSize, lSize;

        MapD();
        MapD(int hSize, int kSize, int lSize);

        double& getPlanDist(const int& h, const int& k, const int& l);
        double& operator()(const int& h, const int& k, const int& l);
};

class MapF: public vector<complex<double>>
{
    public:
        // Размеры F-карты
        int hSize, kSize, lSize = 0;

        MapF();
        MapF(int hSize, int kSize, int lSize);

        complex<double>& getStrAmp(const int& h, const int& k, const int& l);
        complex<double>& operator()(const int& i, const int& j, const int& k);
};

// Карта G-фурье коэффициентов
class MapG
{
    public:
        int hSize, kSize, lSize = 0;

        fftw_plan plan = nullptr;
        fftw_complex* in = nullptr;

        MapG();
        ~MapG();
        MapG(int hSize, int kSize, int lSize);
        
        // ⚠️ ДОБАВЬТЕ ПЕРЕМЕЩАЮЩИЕ ОПЕРАЦИИ
        MapG(MapG&& other) noexcept;
        MapG& operator=(MapG&& other) noexcept;
        
        // ⚠️ ЗАПРЕТИТЕ КОПИРОВАНИЕ (из-за сырых указателей)
        MapG(const MapG&) = delete;
        MapG& operator=(const MapG&) = delete;

        complex<double> getValG(const int& h, const int& k, const int& l);
        complex<double> operator()(const int& h, const int& k, const int& l);

        void setValG(const int& h, const int& k, const int& l, const complex<double>& val); 

        // Производит ее фурье-трансформирование в t-карту
        void transform(MapEta& out);
        void freeMap();
};

// Карта t-векторов
class MapEta : public vector<double>
{
    public:
        int xSize, ySize, zSize = 0;

        fftw_complex* out = nullptr;

        MapEta();
        MapEta(int xSize, int ySize, int zSize);

        ~MapEta();

        MapEta(MapEta&& other) noexcept;
        MapEta& operator=(MapEta&& other) noexcept;
        
        MapEta(const MapEta&) = delete;
        MapEta& operator=(const MapEta&) = delete;

        // Получаем значение Эты в сетке. Где каждый индекс умножаетя на вектор шага
        complex<double> getEta(const int& aGridIndex, const int& bGridIndex, const int& cGridIndex) const;
        void setEta(const int& aGridIndex, const int& bGridIndex, const int& cGridIndex, const complex<double>& newVal);
        void freeMap();
};


#endif