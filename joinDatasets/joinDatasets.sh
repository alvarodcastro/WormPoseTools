#!/bin/bash

if [ $# -gt 1 ]
then
    newDataset='./joinedDataset'
    echo "Joining $@ at ${newDataset}"
    mkdir $newDataset
    if [ $? -eq 0 ]
    then
        for dataset in $@ ;
        do
            for folder in $( ls $dataset );
            do
                mkdir $newDataset/$folder 2> /dev/null
                for dataSplit in $( ls $dataset/$folder ) ;
                do
                    mkdir $newDataset/$folder/$dataSplit 2>/dev/null

                    # Copy first dataset
                    for file in $( ls $dataset/$folder/$dataSplit ) ;
                    do
                        newfile=$(echo ${dataset%/} | rev | cut -d "/" -f1 | rev)
                        echo "copy ${dataset%/}/${folder}/${dataSplit}/${file} to ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}"
                        cp ${dataset%/}/${folder}/${dataSplit}/${file} ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}
                    done
                done
            done
        done
    else
        echo "Exiting process"
    fi

else
    echo "Not valid args"
fi