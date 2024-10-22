#!/bin/bash

parent_process=$(ps -o comm= -p $PPID)

if [[ "$parent_process" == "python" || "$parent_process" == "python3" ]]; then
    echo "\nThere are missing dependencies necessary to start the program."
    echo "These dependencies cannot be automatically installed by the base installer."

    read -p "Do you want to install the missing dependencies? (yes/no): " response

    if [[ "$response" == "yes" ]]; then
        if [[ -f "requirements.txt" ]]; then
            echo "Reading dependencies from requirements.txt..."

            install=false
            while IFS= read -r line; do
                if [[ "$line" == *"# Package required (not automatically installed)"* ]]; then
                    install=true
                elif [[ "$line" == *"# Package required (automatically installed)"* ]]; then
                    install=false
                fi

                if [[ "$install" == true && ! "$line" =~ ^# ]]; then
                    echo "Installing dependency: $line"
                    pip install "$line"
                fi
            done < "requirements.txt"

            echo "Restarting Python program..."
            python3 yourlab/
            exit 0
        else
            echo "requirements.txt not found."
            exit 1
        fi
    else
        echo "Dependency installation canceled. Exiting the program."
        exit 0
    fi
else
    exit 1
fi
