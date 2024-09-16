# rent-a-car-with-python || python ile araba kiralama otomasyon programı

## Dil & Language
- [Türkçe](#programın-amacı)
- [English](#purpose-of-the-program)

## Programın Amacı:

Bu program, bir araba kiralama şirketinin müşteri ve araç bilgilerini kaydedebileceği, araç kiralama işlemlerini gerçekleştirebileceği ve bu işlemleri veritabanına kaydedebileceği bir otomasyon programıdır.

## Kullanılan Teknolojiler:
- Python
- Tkinter
- Mysql
- tkcalendar

## Kurulum:
1. Programı çalıştırabilmek için bilgisayarınızda Python yüklü olmalıdır. Python yüklü değilse [buradan](https://www.python.org/downloads/) indirebilirsiniz.
2. Programın çalışabilmesi için Mysql sunucusunun çalışıyor olması gerekmektedir. Mysql sunucusu çalışmıyorsa [buradan](https://dev.mysql.com/downloads/mysql/) indirebilirsiniz. (veya halihazırda [XAMP](https://www.apachefriends.org/) kullanıyorsanız programın içinden mysql sunucunuzu başlatabilirsiniz).
3. Repoyu klonlayın
```bash
git clone https://github.com/hamer1818/rent-a-car-with-python.git
```
4. Önerilen Kurulum:
    - Programı çalıştırmak için `venv` yani sanal ortamı oluşturmanızı öneriyorum. Bunun için terminalinizi açın ve programın bulunduğu dizine gidin.
    - Ardından aşağıdaki komutları sırasıyla çalıştırın:
    ```bash
    python -m venv venv
    ```
    - Windows için:
    ```bash
    venv\Scripts\activate
    ```
    - Linux için:
    ```bash
    source venv/bin/activate
    ```
    - Son olarak:
    ```bash
    pip install -r requirements.txt
    ```
5. Programı çalıştırmak için terminalinizi açın ve programın bulunduğu dizine gidin. Ardından aşağıdaki komutu çalıştırın:
```bash
python main.py
```


## Hatalar:
> Giriş Ekranı Bozuk


## Purpose of the Program:

This program is an automation program where a car rental company can save customer and vehicle information, perform vehicle rental transactions, and save these transactions to the database.

## Technologies Used:
- Python
- Tkinter
- Mysql
- tkcalendar

## Installation:
1. To run the program, Python must be installed on your computer. If Python is not installed, you can download it from [here](https://www.python.org/downloads/).
2. Mysql server must be running for the program to work. If the Mysql server is not running, you can download it from [here](https://dev.mysql.com/downloads/mysql/). (or if you are already using [XAMP](https://www.apachefriends.org/), you can start your mysql server from the program).
3. Clone the repo
```bash
git clone https://github.com/hamer1818/rent-a-car-with-python.git
```
4. Suggested Installation:
    - I recommend creating a `venv` or virtual environment to run the program. To do this, open your terminal and go to the directory where the program is located.
    - Then run the following commands in order:
    ```bash
    python -m venv venv
    ```
    - For Windows:
    ```bash
    venv\Scripts\activate
    ```
    - For Linux:
    ```bash
    source venv/bin/activate
    ```
    - Finally:
    ```bash
    pip install -r requirements.txt
    ```
5. To run the program, open your terminal and go to the directory where the program is located. Then run the following command:
```bash
python main.py
```
