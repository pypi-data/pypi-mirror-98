## Classical density functional theory code: 1D version (cdft1d)
#### Marat Valiev and Gennady Chuev
___
Simulates inhomogenous molecular liquid system in the presence of
Lennard-Jones (LJ) solute particle

In this release only RISM solver is provided.

The program can be ran as

    rism <input_file>
    
The input file is of the following form

    <solute>
    # site   sigma(Angs)  eps(kj/mol)    charge(e)
    Na       2.16         1.4755         1.0
    <simulation>
    temp 300
    solvent 2site
    tol 1.0E-7
    max_iter 100 
    
It contains two sections: _\<solute\>_ and _\<simulation\>_.

The _\<solute\>_ section specifies solute parameters: name, LJ parameters
and charge.

The _\<simulation\>_ section describes general parameters of the system

    temp 300       - temperature in K (in this case 300K)
    solvent 2site  - solvent model (in this case two site water model)
    tol 1.0E-7     - tolerance for convergence (1.0E-7 in this case)
    max_iter 100   - maximum number of iterations (100 in this case)
    
Upon successfull the program will generate RDF files (with
extension rdf). 
In particular, 
for the example provided above the following rdf files will be generated

    NaH.rdf		NaO.rdf	 
    
The rdf files contains two column - distance (r) and RDF g(r). E.g.

    # r        g(r)
    0.005      0.0
    0.015      7.973e-10
    0.025      2.395e-09
    0.035      4.797e-09
    0.045      8.01e-09
    0.055      1.204e-08
    ....


#### Available solvent models:

    2site
    
    Kippi M. Dyer, John S. Perkyns, George Stell, 
    and B. Montgomery Pettitt,Mol Phys. 2009 ; 107(4-6): 423–431. doi:10.1080/00268970902845313.

#### References:

Gennady N Chuev, Marina V Fedotova and Marat Valiev,
 Renormalized site density functional theory,
 J. Stat. Mech. (2021) 033205

Chuev GN, Fedotova MV, Valiev M. 
Chemical bond effects in classical site density 
functional theory of inhomogeneous molecular liquids. 
J Chem Phys. 2020 Jan 31;152(4):041101. doi: 10.1063/1.5139619. PMID: 32007044.

Marat Valiev and Gennady N Chuev,
 Site density models of inhomogeneous classical molecular liquids,
 J. Stat. Mech. (2018) 093201
 
 