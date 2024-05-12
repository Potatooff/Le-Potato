# Le Potato

**Simple. elegant LLM Chat Inference**

## Get it working

* **Open up your terminal (mac/linux) / powershell terminal (window) and navigate to the project directory**

* **First of all to be safe, let's create a virtual environment!**

    <details>
    <summary>Install on Windows</summary>

    ```bash
    python -m venv .venv
    ```  

    </details>
    <details>
    <summary>Install on Linux / MacOs</summary>

    ```bash
    python3 -m venv .venv
    ```

    </details>

* **Now we need to activate it to be able to use Le Potato without libraries error!**
    <details>
    <summary>Install on Windows</summary>

    ```bash
    .venv\Scripts\activate.ps1
    ```  

    </details>
    <details>
    <summary>Install on Linux / MacOs</summary>

    ```bash
    source .venv/bin/activate
    ```

    </details>

* **Now we are inside our virtual environment...You will have to install all python libraries to be able to use the web app by using:**

    <details>
    <summary>Install on Windows</summary>

    ```bash
    pip install .
    ```  

    </details>
    <details>
    <summary>Install on Linux / MacOs</summary>

    ```bash
    pip3 install .
    ```

    </details>

* **While it is installing, you should check and modify the configuration file**  
**There you will find some samplers and other settings to modify to host model...**

```python
database/configuration.yaml
```

* **Once you are done, you can launch the web server if the libraries are done installing!**

    <details>
    <summary>Install on Windows</summary>

    ```bash
    python main.py
    ```  

    </details>
    <details>
    <summary>Install on Linux / MacOs</summary>

    ```bash
    python3 main.py
    ```

    </details>

* **Once it is all set you can open the website url, by default it is**

```bash
http://127.0.0.1:1234/
```

It will look like this:

![Le Potato - Home Page](database/demos/demo_home_page.png)

Here is a demo of a normal chat

![alt text](database/demos/demo_classic_page.png)

* **You can change the background if you dont like it by going to:**

```bash
  src\frontend\static\images
```

**There you will drop your background you wanted and just rename it toji.jpg to make it easier.**

---  
**How to use the RAG from the UI?**

* You need to add `-rag` followed with your rag query that will be used for the retrieval. (Will not be showed to the model  )

* Then you add a new line and write down your query for the model.

Example:
```
-rag Who is the author?
Do you know the author ?  
```

*LLM will only see the second line and the rag query will add retrieval results to your query!*

### Here you go all set, Have fun! If you had issues dont hesitate to report it on the repo | I mainly used the UI with OpenAI compatible url
