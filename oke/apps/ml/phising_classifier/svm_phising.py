import re
import csv
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from newspaper import Article
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
    
class PhisingClassifier:

    def lowercase(self,berita):
        lower_case = berita.lower()
        return lower_case

    def removenumber(self,berita):
        hasil = re.sub(r"\d+", "", berita)
        return hasil

    def repunctuation(self,berita):
        hasil = berita.translate(str.maketrans("","",string.punctuation))
        return hasil

    def whitespace(self,berita):
        hasil = berita.strip()
        return hasil

    def stopword(self,berita):
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        hasil = stopword.remove(berita)
        return hasil

    def stemming(self,berita):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return stemmer.stem(berita)

#Read the data one by one and process it

    def preprocessingdata():
        hasil = []

        with open('dataset.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                kelas = row["sentimen"]
                teks = row["berita"]
                hlowercase = lowercase(teks)
                hremovenumber = removenumber(hlowercase)
                hrepunctuation = repunctuation(hremovenumber)
                hwhitespace = whitespace(hrepunctuation)
                hstopword = stopword(hwhitespace)
                hasilStemming = stemming(hstopword)
                hasil.append((kelas,hasilStemming))
                line_count += 1
   
  
        with open('hasilPreprocess2.csv', 'w') as f:
        writer = csv.writer(f,delimiter=',',lineterminator='\n')
        for line in hasil:
            writer.writerow(line)
            

    def scrappingberita(self,url):
        article = Article(url,'id')
        article.download()
        article.parse()
        judul = article.title
        return judul
    
    
    def prediksi(self,urlhoax):
        url = urlhoax
        
        judul = self.scrappingberita(url)
        hlowercase = self.lowercase(judul)
        hremovenumber = self.removenumber(hlowercase)
        hrepunctuation = self.repunctuation(hremovenumber)
        hwhitespace = self.whitespace(hrepunctuation)
        hstopword = self.stopword(hwhitespace)
        hasilStemming = self.stemming(hstopword)
                          
        namaFile = "hasilPreprocess2.csv"
        data = []
        label = []
        with open(namaFile, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader) #skip header
            for row in reader:
                data.append(row[1])
                label.append(row[0])
 

        X_train = data
        y_train = label
 
 
        #transform ke tfidf dan train dengan naive bayes

        text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
        text_clf.fit(X_train, y_train)

        # coba prediksi data baru
        sms_baru = [hasilStemming]
        pred = text_clf.predict(sms_baru)
        #print("Hasil prediksi {}".format(pred))
        
      return pred
