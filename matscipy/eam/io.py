#! /usr/bin/env python

# ======================================================================
# matscipy - Python materials science tools
# https://github.com/libAtoms/matscipy
#
# Copyright (2014) James Kermode, King's College London
#                  Lars Pastewka, Karlsruhe Institute of Technology
#                  Adrien Gola, Karlsruhe Institute of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# ======================================================================


from __future__ import division, print_function

import numpy as np
try:
    from scipy import interpolate
except:
    print('Warning: No scipy')
    interpolate = False

import os

###

def read_eam(eam_file):
    """
    Read an eam alloy lammps format file and return the tabulated data and parameters
    http://lammps.sandia.gov/doc/pair_eam.html
    
    Parameters
    ----------
      eam_alloy_file : string
                      eam alloy file name 
    Returns
    -------
      source : string
          Source informations or comment line for the file header
      parameters : array_like
                [0] - array of int - atomic numbers
                [1] - array of float -atomic masses
                [2] - array of float - equilibrium lattice parameter
                [3] - array of str - crystal structure
                [4] - int - number of data point for embedded function
                [5] - int - number of data point for density and pair functions
                [6] - float - step size for the embedded function
                [7] - float - step size for the density and pair functions
                [8] - float - cutoff of the potentials
      F : array_like
          contain the tabulated values of the embedded functions
          shape = (nb atoms,nb atoms, nb of data points)
      f : array_like
          contain the tabulated values of the density functions
          shape = (nb atoms,nb atoms, nb of data points)
      rep : array_like
          contain the tabulated values of pair potential
          shape = (nb atoms,nb atoms, nb of data points)
    """
    eam = open(eam_file,'r').readlines()
    # reading 3 first comment lines as source for eam potential data
    source = eam[0].strip()
    # -- Parameters -- #
    atnumber = int(eam[1].split()[0])
    atmass = float(eam[1].split()[1])
    crystallatt = float(eam[1].split()[2])
    crystal = eam[1].split()[3]
    Nrho = int(eam[2].split()[0])       # Nrho (number of values for the embedding function F(rho))
    Nr = int(eam[2].split()[2])         # Nr (number of values for the effective charge function Z(r) and density function rho(r))
    drho = float(eam[2].split()[1])     # spacing in density space
    dr = float(eam[2].split()[3]) # spacing in distance space
    cutoff = float(eam[2].split()[4])
    parameters = np.array([atnumber, atmass,crystallatt,crystal, Nrho,Nr, drho, dr, cutoff])
    # -- Tabulated data -- #
    data = np.loadtxt(eam_file, dtype="float", skiprows = 3).flatten()
    F = data[0:Nrho]
    f = data[Nrho:Nrho+Nr]
    rep = data[Nrho+Nr:2*Nr+Nrho]
    return source,parameters, F,f,rep

def read_eam_alloy(eam_alloy_file):
    """
    Read an eam alloy lammps format file and return the tabulated data and parameters
    http://lammps.sandia.gov/doc/pair_eam.html
    
    Parameters
    ----------
      eam_alloy_file : string
                      eam alloy file name 
    Returns
    -------
      source : string
          Source informations or comment line for the file header
      parameters : array_like
                [0] - array of str - atoms 
                [1] - array of int - atomic numbers
                [2] - array of float -atomic masses
                [3] - array of float - equilibrium lattice parameter
                [4] - array of str - crystal structure
                [5] - int - number of data point for embedded function
                [6] - int - number of data point for density and pair functions
                [7] - float - step size for the embedded function
                [8] - float - step size for the density and pair functions
                [9] - float - cutoff of the potentials
      F : array_like
          contain the tabulated values of the embedded functions
          shape = (nb atoms, nb of data points)
      f : array_like
          contain the tabulated values of the density functions
          shape = (nb atoms, nb of data points)
      rep : array_like
          contain the tabulated values of pair potential
          shape = (nb atoms,nb atoms, nb of data points)
    """
    eam = open(eam_alloy_file,'r').readlines()
    # reading 3 first comment lines as source for eam potential data
    source = eam[0].strip()+eam[1].strip()+eam[2].strip()
    # -- Parameters -- #
    atoms = eam[3].strip().split()[1:]
    nb_atoms = len(atoms)
    Nrho = int(eam[4].split()[0])       # Nrho (number of values for the embedding function F(rho))
    Nr = int(eam[4].split()[2])         # Nr (number of values for the effective charge function Z(r) and density function rho(r))
    drho = float(eam[4].split()[1])     # spacing in density space
    dr = float(eam[4].split()[3]) # spacing in distance space
    cutoff = float(eam[4].split()[4])
    atnumber,atmass,crystallatt,crystal = np.empty(nb_atoms,dtype=int),np.empty(nb_atoms),np.empty(nb_atoms),np.empty(nb_atoms).astype(np.str)
    for i in range(nb_atoms):
        l = len(eam[6].strip().split())
        row = int(5+i*((Nr+Nrho)/l+1))
        atnumber[i] = int(eam[row].split()[0])
        atmass[i] = float(eam[row].split()[1])
        crystallatt[i] = float(eam[row].split()[2])
        crystal[i] = str(eam[row].split()[3])
    parameters = (atoms, atnumber, atmass,crystallatt,crystal, Nrho,Nr, drho, dr, cutoff)
    # -- Tabulated data -- #
    F,f,rep,data = np.empty((nb_atoms,Nrho)),np.empty((nb_atoms,Nr)),np.empty((nb_atoms,nb_atoms,Nr)),np.empty(())
    eam = open(eam_alloy_file,'r')
    [eam.readline() for i in range(5)]
    for i in range(nb_atoms):
        eam.readline()
        data = np.append(data,np.fromfile(eam,count=Nrho+Nr, sep=' '))
    data = np.append(data,np.fromfile(eam,count=-1, sep=' '))
    data = data[1:]
    for i in range(nb_atoms):
        F[i,:] = data[i*(Nrho+Nr):Nrho+i*(Nrho+Nr)]
        f[i,:] = data[Nrho+i*(Nrho+Nr):Nrho+Nr+i*(Nrho+Nr)]
    interaction = 0
    for i in range(nb_atoms):
        for j in range(nb_atoms):
            if j < i :
                rep[i,j,:] = data[nb_atoms*(Nrho+Nr)+interaction*Nr:nb_atoms*(Nrho+Nr)+interaction*Nr+Nr]
                interaction+=1
        rep[i,i,:] = data[nb_atoms*(Nrho+Nr)+interaction*Nr:nb_atoms*(Nrho+Nr)+interaction*Nr+Nr]
        interaction+=1
    return source,parameters, F,f,rep

def mix_eam_alloy(files):
    """
    mix eam alloy files data set and compute the interspecies pair potential part using the 
    mean geometric value from each pure species 
    
    Parameters
    ----------
      files : array of strings
              Contain all the files to merge and mix
    Returns
    -------
      sources : string
          Source informations or comment line for the file header
      parameters_mix : array_like
                [0] - array of str - atoms 
                [1] - array of int - atomic numbers
                [2] - array of float -atomic masses
                [3] - array of float - equilibrium lattice parameter
                [4] - array of str - crystal structure
                [5] - int - number of data point for embedded function
                [6] - int - number of data point for density and pair functions
                [7] - float - step size for the embedded function
                [8] - float - step size for the density and pair functions
                [9] - float - cutoff of the potentials
      F_ : array_like
          contain the tabulated values of the embedded functions
          shape = (nb atoms,nb atoms, nb of data points)
      f_ : array_like
          contain the tabulated values of the density functions
          shape = (nb atoms,nb atoms, nb of data points)
      rep_ : array_like
          contain the tabulated values of pair potential
          shape = (nb atoms,nb atoms, nb of data points)
    """
    nb_at = 0
    # Counting elements and repartition and select smallest tabulated set Nrho*drho // Nr*dr
    Nrho,drho,Nr,dr,cutoff = np.empty((len(files))),np.empty((len(files))),np.empty((len(files))),np.empty((len(files))),np.empty((len(files)))
    sources = ""
    for i,f in enumerate(files):
        source,parameters, F,f,rep = read_eam_alloy(f)
        sources+= source
        source += " "
        nb_at+=len(parameters[0])
        Nrho[i] = parameters[5]
        drho[i] = parameters[7]
        cutoff[i] = parameters[9]
        Nr[i] = parameters[6]
        dr[i] = parameters[8]
    min_cutoff = cutoff.argmin()
    min_prod = (Nrho*drho).argmin()
    # only taking into account the self repulsive function for each atom, no intespecies repulsive function if existing
    rep_list = [0,2,5,9,14]
    idx_list = [1,3,4,6,7,8,10,11,12,13,14]
    F_,f_,rep_ = np.empty((nb_at,nb_at,Nrho[min_prod])),np.empty((nb_at,nb_at,Nr[min_cutoff])),np.empty((nb_at,nb_at,Nr[min_cutoff]))
    atnumber,atmass,crystallatt,crystal,atoms = np.empty(0),np.empty(0),np.empty(0),np.empty(0).astype(np.str),np.empty(0).astype(np.str)
    Nrho_ = Nrho[min_prod]
    Nr_ = Nr[min_cutoff]
    drho_ = drho[min_prod]
    dr_ = dr[min_cutoff]
    n_at,n_rep = 0,0
    for j,f in enumerate(files):
        source,parameters, F,f,rep = read_eam_alloy(f)
        atoms = np.append(atoms,parameters[0])
        atnumber = np.append(atnumber,parameters[1])
        atmass = np.append(atmass,parameters[2])
        crystallatt = np.append(crystallatt,parameters[3])
        crystal = np.append(crystal,parameters[4])
        for i in range(len(parameters[0])):
            F_[n_at,n_at,:] = interpolate.InterpolatedUnivariateSpline(np.linspace(0,Nrho[j]*drho[j],Nrho[j]),F[i,:])(np.linspace(0,Nrho_*drho_,Nrho_))
            f_[n_at,n_at,:] = interpolate.InterpolatedUnivariateSpline(np.linspace(0,Nr[j]*dr[j],Nr[j]),f[i,:])(np.linspace(0,Nr_*dr_,Nr_))
            rep_[n_at,n_at,:] = interpolate.InterpolatedUnivariateSpline(np.linspace(0,Nr[j]*dr[j],Nr[j]),rep[rep_list[i],:])(np.linspace(0,Nr_*dr_,Nr_))
            n_at+=1
    # mixing repulsive part
    for i in range(nb_at):
        for j in range(nb_at):
            if j > i :
              rep_[i,j,:] = np.sqrt(np.abs(rep_[i,i,:]*rep_[j,j,:]))

    parameters_mix = np.array((atoms, atnumber, atmass,crystallatt,crystal, Nrho_,Nr_, drho_, dr_, cutoff[min_cutoff]))
    return sources, parameters_mix, F_, f_, rep_
  
def write_eam_alloy(source, parameters, F, f, rep,out_file):
    """
    Write an eam alloy lammps format file 
    http://lammps.sandia.gov/doc/pair_eam.html
    
    Parameters
    ----------
    source : string
          Source information or comment line for the file header
    parameters : array_like
                [0] - array of str - atoms 
                [1] - array of int - atomic numbers
                [2] - array of float -atomic masses
                [3] - array of float - equilibrium lattice parameter
                [4] - array of str - crystal structure
                [5] - int - number of data point for embedded function
                [6] - int - number of data point for density and pair functions
                [7] - float - step size for the embedded function
                [8] - float - step size for the density and pair functions
                [9] - float - cutoff of the potentials
    F : array_like
        contain the tabulated values of the embedded functions
        shape = (nb atoms, nb of data points)
    f : array_like
        contain the tabulated values of the density functions
        shape = (nb atoms, nb of data points)
    rep : array_like
        contain the tabulated values of pair potential
        shape = (nb atoms,nb atoms, nb of data points)
    out_file : string
              output file name for the eam alloy potential file
    Returns
    -------
      
    """
    atoms,atnumber,atmass,crystallatt,crystal = parameters[0],parameters[1],parameters[2],parameters[3],parameters[4]
    Nrho,Nr, drho, dr, cutoff = parameters[5],parameters[6],parameters[7],parameters[8],parameters[9]  
    # parameters unpacked
    atlines = []
    for i,at in enumerate(atoms):
        atlines.append('%i\t%f\t%f\t%s\n'%(atnumber[i],atmass[i],crystallatt[i],crystal[i]))
    pottitle = "# Mixed EAM alloy potential from :\n#%s \n#\n"%(source)
    # --- Writing new EAM alloy pot file --- #
    potfile = open(out_file,'w')
    potfile.write(pottitle)
    potfile.write('%i '%len(atoms))
    for at in atoms:
        potfile.write(at+' ')
    potfile.write('\n')
    potfile.write('%i\t%e\t%i\t%e\t%e\n'%(Nrho,drho,Nr,dr,cutoff))
    for i,at in enumerate(atoms):
        potfile.write(atlines[i])
        for j in F[i,:]:
            potfile.write("%.16e \n"%j)
        for j in f[i,:]:
            potfile.write("%.16e \n"%j)
    for i in range(len(rep)):
        for j in range(len(rep)):
            if j < i :
                for h in rep[i,j,:]:
                    potfile.write("%.16e \n"%h)
        for h in rep[i,i,:]:
            potfile.write("%.16e \n"%h)

    potfile.close()  
    
def write_eam(source, parameters, F, f, rep,out_file):
    """
    Write an eam lammps format file 
    http://lammps.sandia.gov/doc/pair_eam.html
    
    Parameters
    ----------
    source : string
	  Source information or comment line for the file header
    parameters : array_like
		[0] - array of int - atomic numbers
		[1] - array of float -atomic masses
		[2] - array of float - equilibrium lattice parameter
		[3] - array of str - crystal structure
		[4] - int - number of data point for embedded function
		[5] - int - number of data point for density and pair functions
		[6] - float - step size for the embedded function
		[7] - float - step size for the density and pair functions
		[8] - float - cutoff of the potentials
    F : array_like
	contain the tabulated values of the embedded functions
	shape = (nb of data points)
    f : array_like
	contain the tabulated values of the density functions
	shape = (nb of data points)
    rep : array_like
	contain the tabulated values of pair potential
	shape = (nb of data points)
    out_file : string
	      output file name for the eam alloy potential file
    Returns
    -------
      
    """
    atnumber,atmass,crystallatt,crystal = parameters[0],parameters[1],parameters[2],parameters[3]
    Nrho,Nr, drho, dr, cutoff = parameters[4],parameters[5],parameters[6],parameters[7],parameters[8]
    # parameters unpacked
    atline = "%i %f %f %s\n"%(int(atnumber),float(atmass),float(crystallatt),str(crystal))
    pottitle = "# EAM potential from : # %s \n"%(source)
    # --- Writing new EAM alloy pot file --- #
    potfile = open(out_file,'w')
    potfile.write(pottitle)
    potfile.write(atline)
    potfile.write('%i\t%.16e\t%i\t%.16e\t%.10e\n'%(int(Nrho),float(drho),int(Nr),float(dr),float(cutoff)))
    for i in F:
	potfile.write("%.16e \n"%i)
    for i in f:
	potfile.write("%.16e \n"%i)
    for i in rep:
	potfile.write("%.16e \n"%i)

    potfile.close()  