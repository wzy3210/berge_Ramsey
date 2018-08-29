# berge_Ramsey
This repository contains the code that verifies some of the base cases in the paper 
"Ramsey numbers of Berge-hypergraphs and related structures" by Nika Salia, Casey Tompkins, Zhiyu Wang and Oscar Zamora.

There are two main files: Ramsey_3uniform.py and Ramsey_4uniform.py

1. Ramsey_3uniform.py aims to verify that R^3(BK4, BK5) <= 6. Running time is usually within 5 mins.
2. Ramsey_4uniform.py aims to verify that R^4(BK6, BK6) <= 7. Running time could take up to 2-5 days depending on the machine.

Both of the files use a library to find size of a maximal matching of a bipartite graph. 
The library is written by David Eppstein, UC Irvine, in 27 Apr 2002. We are deeply grateful for this library.

Maintainer: Zhiyu Wang 
Email: zhiyuw@math.sc.edu

Please contact the maintainer if you find any bug in the code or fail to reproduce the results.

