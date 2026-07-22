/*
PSS 2. Paul D. Drozhilkin

В данном файле представлен набор небольших функций для работы с простой математикой.
Например, перевод в градусы и радианы, вывод с округлением, проверка знаков,
А также перевод обычных дробей из .cif-файлов в десятичные для расчетов
*/

#ifndef BASIC_MATH
#define BASIC_MATH

#include "pss2_basic_types.hpp"
#include "pss2_static_consts.hpp"

inline double toDeg(double rad) 
{ 
    return (rad * 180.00000) / Consts::Pi; 
}

inline double toRad(double deg) 
{ 
    return (deg * Consts::Pi) / 180.000000; 
}

inline string strRoundTo(double num, int digits)
{
    std::ostringstream buf;
    
    const double factor = std::pow(10, digits);
    const double val = std::round(num * factor) / factor;

    if (num < 0.0) buf << std::fixed << std::setprecision(digits) << val;
    else buf << " " << std::fixed << std::setprecision(digits) << val;
    
    return buf.str();
}

inline bool isSign(const char& symbol) 
{ 
    return ((symbol == '+') || (symbol == '-')); 
}

inline bool isFrac(const string& symbol) 
{ 
    return isdigit(symbol[0]); 
}

inline double toSign(const char& sign)
{
    if (sign == '+') return 1.000;
    else if (sign == '-') return -1.0000;
    else return 0;
}

inline bool isZero(double x, double epsilon = Consts::ZERO_PRECISION) 
{ 
    return std::abs(x) < epsilon; 
}

inline double toFrac(const string& frac)
{
    const size_t slash_pos = frac.find('/');

    const double a = stod(frac.substr(0, slash_pos));
    const double b = stod(frac.substr(slash_pos + 1));

    return a / b;
}

#endif