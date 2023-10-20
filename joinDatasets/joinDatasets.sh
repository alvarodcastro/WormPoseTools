#!/bin/bash

if [ $# -eq 2 ]
then
    newDataset='./joinedDataset'
    echo "Joining ${1} with ${2} at ${newDataset}"
    mkdir $newDataset
    if [ $? -eq 0 ]
    then
        for folder in $( ls $1 );
        do
            mkdir $newDataset/$folder
            for dataSplit in $( ls $1/$folder ) ;
            do
                mkdir $newDataset/$folder/$dataSplit

                # Copy first dataset
                for file in $( ls $1/$folder/$dataSplit ) ;
                do
                    newfile=$(echo ${1%/} | rev | cut -d "/" -f1 | rev)
                    echo "copy ${1%/}/${folder}/${dataSplit}/${file} to ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}"
                    cp ${1%/}/${folder}/${dataSplit}/${file} ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}
                done

                # Copy second dataset
                for file in $( ls $2/$folder/$dataSplit ) ;
                do
                    newfile=$(echo ${2%/} | rev | cut -d "/" -f1 | rev)
                    echo "copy ${2%/}/${folder}/${dataSplit}/${file} to ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}"
                    cp ${2%/}/${folder}/${dataSplit}/${file} ${newDataset}/${folder}/${dataSplit}/${newfile}_${file}
                done
            done
        done
    else
        echo "Exiting process"
    fi

else
    echo "Not valid args"
fi