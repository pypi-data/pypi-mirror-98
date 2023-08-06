#
# examples for SourceUndulator to be used in ShadowOui
#

import os
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from orangecontrib.shadow.util.undulator.SourceUndulator import SourceUndulator
from Shadow import Beam as Shadow3Beam


if __name__ == "__main__":

    do_plots = True
    #
    # syned
    #
    su = Undulator.initialize_as_vertical_undulator(K=0.25,period_length=0.032,periods_number=50)

    ebeam = ElectronBeam(energy_in_GeV=6.04,
                 energy_spread = 0.0,
                 current = 0.2,
                 number_of_bunches = 400,
                 moment_xx=(400e-6)**2,
                 moment_xxp=0.0,
                 moment_xpxp=(10e-6)**2,
                 moment_yy=(10e-6)**2,
                 moment_yyp=0.0,
                 moment_ypyp=(4e-6)**2 )

    sourceundulator = SourceUndulator(name="test",syned_electron_beam=ebeam,syned_undulator=su,
                    flag_emittance=1,flag_size=0,
                    emin=10490.0,emax=10510.0,ng_e=3,
                    maxangle=0.015,ng_t=51,ng_p=11,ng_j=20,
                    code_undul_phot="pySRU")


    sourceundulator.set_energy_monochromatic_at_resonance(0.98)

    print(sourceundulator.info())

    #
    # plot
    #
    if do_plots:
        from srxraylib.plot.gol import plot_image, plot_scatter

        radiation,photon_energy, theta,phi = sourceundulator.get_radiation_polar()
        plot_image(radiation[0],1e6*theta,phi,aspect='auto',title="intensity",xtitle="theta [urad]",ytitle="phi [rad]")

        radiation_interpolated,photon_energy, vx,vz = sourceundulator.get_radiation_interpolated_cartesian()
        plot_image(radiation_interpolated[0],vx,vz,aspect='auto',title="intensity interpolated in cartesian grid",xtitle="vx",ytitle="vy")

        polarization = sourceundulator._result_radiation["polarization"]
        plot_image(polarization[0],1e6*theta,phi,aspect='auto',title="polarization",xtitle="theta [urad]",ytitle="phi [rad]")


    # beam = sourceundulator.calculate_shadow3_beam(user_unit_to_m=1.0,F_COHER=0,NRAYS=15000,SEED=5655452)
    rays = sourceundulator.calculate_rays(user_unit_to_m=1.0,F_COHER=0,NRAYS=15000,SEED=5655452)

    print(sourceundulator.info())

    for k in sourceundulator._result_radiation.keys():
        print(k)

    #
    # write shadow3 beam and file
    #

    shadow3_beam = Shadow3Beam(N=rays.shape[0])

    shadow3_beam.rays = rays

    os.system("rm -f begin.dat start.00 end.00")
    shadow3_beam.write("begin.dat")
    print("File written to disk: begin.dat")



    print("Beam intensity: ",shadow3_beam.getshcol(23).sum())
    print("Beam intensity s-pol: ",shadow3_beam.getshcol(24).sum())
    print("Beam intensity: p-pol",shadow3_beam.getshcol(25).sum())

    #
    # plot
    #
    if do_plots:
        plot_scatter(1e6*shadow3_beam.rays[:,0],1e6*shadow3_beam.rays[:,2],title="real space",xtitle="X [um]",ytitle="Z [um]",show=False)
        plot_scatter(1e6*shadow3_beam.rays[:,3],1e6*shadow3_beam.rays[:,5],title="divergence space",xtitle="X [urad]",ytitle="Z [urad]",show=True)

