# Air Quality Stations Dashboard 

![image](https://github.com/SyafiqMSI/analisis-air-quality/blob/main/data/image.png)

[Air Quality Station Analysis ](https://airquality-msi.streamlit.app/) adalah sebuah proyek yang bertujuan untuk menganalisis kualitas udara melalui data yang dikumpulkan dari stasiun-stasiun. Proyek ini menyajikan informasi mengenai suhu, kecepatan angin, serta parameter penting lainnya yang berkaitan dengan kualitas udara untuk membantu pengguna dalam memahami kondisi lingkungan di sekitar mereka dari data-data tahun sebelumnya.

Anda bisa mengakses link (https://airquality-msi.streamlit.app/) atau jika ingin menjalankan di lokal komputer silahkan ikuti langkah-langkah di bawah

## Setup Environment - Shell/Terminal
```
cd analisis-air-quality
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Run steamlit app - Shell/Terminal
```
cd .\dashboard\
python -m streamlit run dashboard.py
```

## Run steamlit app -Anaconda Prompt
```
cd .\dashboard\
streamlit run dashboard.py
```
