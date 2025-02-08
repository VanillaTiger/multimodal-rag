# multimodal-rag

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Everything from main multimodal-rag directory


1. To scrape the Articles run

```python
python3 scripts/scraper_batch_news.py
```

2. To download all images from the scraped data

```python
python3 scripts/download_img.py
```

3. in secrets folder create **secret.txt** file that have OPENAI KEY in the first line.
```
**-****-*****************************************************************
```

4. Create Vector Database
```
python3 src/db_manager.py --create_db
```

5. Run streamlit APP
```bash
streamlit run app.py
```

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501

6. Enter The App

You can write a question and get answer in the format:

```
DeepSeek is an open model, similar to OpenAI's o1, that is used for language and multimodal tasks. Its license allows for the use and modification of its outputs, potentially pushing forward the state of the art for language models. DeepSeek released DeepSeek-R1, a large language model that can execute long lines of reasoning without explicit prompting. In tests, it outperformed o1 on 5 out of 11 benchmarks and has shown promise in distilling its reasoning abilities to smaller student models. It also allows for users to see the steps the model takes to arrive at an answer, unlike some other reasoning models.

Sources:

source_file = data_img_str_url.csv in row = 3
article_url = https://www.deeplearning.ai/the-batch/issue-285/
images = https://dl-staging-website.ghost.io/content/images/2025/01/unnamed--45-.gif
```


or change the tab to "Data" and view the source data 