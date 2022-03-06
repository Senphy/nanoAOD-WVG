import os,sys
import shutil
import subprocess

def ALP_batch_condor():
    MassesALP = [50, 90, 100, 110, 160, 200, 300, 400]
    year = 2018
    eospath = '/eos/user/s/sdeng/WZG_analysis/ALP/'
    initial_path = os.getcwd()

    for mass in MassesALP:
        Sample_Name = "ALP_lvlla_4f_LO_m%s" %(str(mass))
        if os.path.isdir(Sample_Name):
            shutil.rmtree(Sample_Name)
        os.makedirs(Sample_Name+'/log')
        if not os.path.isdir(eospath + str(year) + '/' + Sample_Name):
            os.makedirs(eospath + str(year) + '/' + Sample_Name)


        shutil.copyfile('cmssw-cc7.sh', Sample_Name+'/cmssw-cc7.sh')
        shutil.copyfile('filepath_Neutrino_E-10_gun_%s.txt' %(str(year)), Sample_Name+'/filepath_Neutrino_E-10_gun_%s.txt' %(str(year)))
        shutil.copyfile('randomizeSeeds.py', Sample_Name+'/randomizeSeeds.py')
        shutil.copyfile('slc7_active_ALP_production_%s_v9.sh' %(str(year)), Sample_Name+'/slc7_active_ALP_m%s_production_%s_v9.sh' %(str(mass), str(year)))
        shutil.copyfile('submit_ALP_production_%s_v9.jdl' %(str(year)), Sample_Name+'/submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), str(year)))
        shutil.copyfile('wrapper_ALP_production_%s_v9.sh' %(str(year)), Sample_Name+'/wrapper_ALP_m%s_production_%s_v9.sh' %(str(mass), str(year)))
        shutil.copyfile(eospath+'/ALP_lvlla_4f_LO_m%s_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' %(str(mass)), Sample_Name+'/ALP_lvlla_4f_LO_m%s_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' %(str(mass)))

        os.popen('sed -i "s/WRAPPER.sh/wrapper_ALP_m%s_production_%s_v9.sh/g" %s/submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), str(year), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/EXECUTABLE.sh/slc7_active_ALP_m%s_production_%s_v9.sh/g" %s/submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), str(year), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/ROOTNAME/ALP_lvlla_4f_LO_m%s/g" %s/submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/YEAR/%s/g" %s/submit_ALP_m%s_production_%s_v9.jdl' %(str(year), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/TARBALLNAME/ALP_lvlla_4f_LO_m%s_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/g" %s/submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/TARBALLNAME/ALP_lvlla_4f_LO_m%s_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/g" %s/wrapper_ALP_m%s_production_%s_v9.sh' %(str(mass), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/WRAPPER.sh/wrapper_ALP_m%s_production_%s_v9.sh/g" %s/slc7_active_ALP_m%s_production_%s_v9.sh' %(str(mass), str(year), Sample_Name, str(mass), str(year)))
        os.popen('sed -i "s/ROOTNAME/ALP_lvlla_4f_LO_m%s/g" %s/slc7_active_ALP_m%s_production_%s_v9.sh' %(str(mass), Sample_Name, str(mass), str(year)))
        
        # Have some potential bugs here! *FIXME*
        os.chdir(Sample_Name)
        subprocess.call('condor_submit submit_ALP_m%s_production_%s_v9.jdl' %(str(mass), str(year)), shell=True)
        os.chdir(initial_path)

    pass

if __name__ == '__main__':
    ALP_batch_condor()
