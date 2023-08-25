#!/bin/bash


{ # try

     pkill -f firefox
    #save your output

} || { # catch
    echo 'firefox not found'
} 

{ # try

     pkill -f firefox-bin
    #save your output

} || { # catch
    echo 'firefox not found'
} 

{ # try

     pkill -f geckodriver
    #save your output

} || { # catch
    echo 'firefox not found'
} 

{ # try
     pkill -f chrome

} || { # catch
    echo 'chrome not found'
} 

{ # try
     pkill python

} || { # catch
    echo 'python not found'
} 

{ # try
     pkill python3

} || { # catch
    echo 'python3 not found'
} 

{ # try

    rm -rfv ~/Desktop/repo/2022-cookie-accept-all/profiles/openwpm/*
    #save your output

} || { # catch
    echo 'error while removing folders'
} 

{
    rm  -rf ~/Desktop/repo/2022-cookie-accept-all/geckodriver.log
}  || { 
    echo 'could not remove geckodriver.log'
}
 


{ # try

    rm ~/openwpm/openwpm.log
    touch ~/openwpm/openwpm.log 
    #save your output

} || { # catch
    echo 'error while removing openwpm.log'
}  


{ # try

    git pull
    #save your output

} || { # catch
    echo 'git pull error'
} 

   source ~/miniconda3/etc/profile.d/conda.sh &&
   conda activate openwpm &&    
   #pkill -f QueueManager.py  &&
   python3 ~/Desktop/repo/2022-cookie-accept-all/QueueManager.py