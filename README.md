# Prenotami schedule helper
Python bot to log into [prenot@mi](prenotami.esteri.it) and schedule citizenship/passport using Selenium. *** I found an old version of this selenium bot, so I leave it public to anyone who could use it as free or for a reference *** <br>

---

## How to use it:

- Download this repo and create a virtual env. Make use of it and install the required libs.
    ```
    git clone https://github.com/nico98gon/prenotami-1.0.0
    cd prenotami
    python3 -m venv .venv (this create an enviroment for your selenium bot)
    source .venv/bin/activate for Unix OS or .venv\Scripts\activate for Windows OS
    pip install -r requirements.txt
    mkdir files (and upload the files whit the names "identidade.pdf" and "residencia.pdf")
    create in the base of the project a file .env with your:
        username_prenotami=HERE_GO_YOUR_USERNAME
        password_prenotami=HERE_GO_YOUR_PASSWORD
    ```

- Modify the parameters.yaml file to fit your specific needs.

- Add username and password to log in to prenota in the .env file (substitute the ADD_USERNAME_HERE used in the above code).

- Add a file called **residencia.pdf** under the files folder to be uploaded in the scheduling process. This file has to demonstrate that you live in the address that is covered by the consulate you are trying to schedule. For example it can be utility bills (phone, electricity, etc). For passport there is also a need to add the identity file in the same folder, named **identidade.pdf**. 

Then run the bot using:
    .venv\Scripts\activate (this activate the enviroment)
    python __main__.py

And when you finish just deactivate the enviroment:
    deactivate

---

Feel free to contribute/ make your changes to the code. Any questions feel free to raise an issue!
