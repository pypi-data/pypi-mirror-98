# Welcome to qrtt.org

We are trying to develop Python tools for quantitative research and trading hobbyists.





## Speed

Technical indicators in QRTT are calculated using Pandas and Numpy. This choice is consistent with the goal of this project: making quantitative as easy as possible for beginners. 

However, QRTT is much slower compared to its C/C++ or Java based alternatives such as ta-lib. In general, generating calculation-lite indicators (such as SMA) are about 7 ~ 9 times slower compared to ta-lib. For (relatively) computational heavy indicators (such as RSI), QRTT is 25~30 times slower. 

You won't notice any difference if you just generating a few indicators. It only takes a few millisecond for QRTT to generate indicator values (on about 20 years of data of one individual stock). In comparison, it takes a few hundred microseconds (less than 1 millisecond) for ta-lib to do it. This becomes problematic when you need to generate many features for testing. 



## How to use

### Data



### Technical Indicators

