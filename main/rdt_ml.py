import os
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from gensim.models import Word2Vec
from scipy.spatial.distance import jensenshannon
from sklearn.preprocessing import normalize

os.environ["LOKY_MAX_CPU_COUNT"] = "4"

class Analyzer:
    def __init__(self, skill_mapping):
        self.language_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        self.skill_mapping = skill_mapping

    def clean_text(self, text):
        text = re.sub(r'\(?[А-Я]{1,2}-\d\.\d\)?', '', text)
        text = re.sub(r'[^а-яёa-z0-9+#]', ' ', text.lower())
        text += 'высшее образование'
        return re.sub(r'\s+', ' ', text).strip()

    def enhance_skills(self, text):
        for term, related_skills in self.skill_mapping.items():
            if term in text:
                text += ' ' + ' '.join(related_skills)
        return text

    def create_embeddings(self, texts):
        # BERT embeddings
        bert_vectors = self.language_model.encode(texts)
        
        # Word2Vec embeddings
        tokenized = [self.clean_text(t).split() for t in texts]
        word_model = Word2Vec(tokenized, vector_size=100, window=5, min_count=1, workers=4)
        
        # Create average vectors
        word_vectors = []
        for text in tokenized:
            vectors = [word_model.wv[word] for word in text if word in word_model.wv]
            word_vectors.append(np.mean(vectors, axis=0) if vectors else np.zeros(100))
        
        return np.hstack([
            normalize(bert_vectors),
            normalize(np.array(word_vectors))
        ])

    def main_analyze(self, edu_texts, job_texts, metric = 'optimal'):
    # Предобработка текстов
        processed_edu = [self.enhance_skills(self.clean_text(t)) for t in edu_texts]
        processed_jobs = [self.enhance_skills(self.clean_text(t)) for t in job_texts]
        
        # Создание эмбеддингов
        edu_emb = self.create_embeddings(processed_edu)
        jobs_emb = self.create_embeddings(processed_jobs)
        
        # Объединение данных
        all_embeddings = np.vstack([edu_emb, jobs_emb])
        
        # Динамический выбор числа кластеров
        n_samples = all_embeddings.shape[0]
        n_clusters = min(10, max(2, n_samples // 2))  # Не больше 10 и не меньше 2
        
        # Кластеризация
        if n_samples >= n_clusters:
            kmeans = KMeans(n_clusters=n_clusters)
            clusters = kmeans.fit_predict(all_embeddings)
            
            # Расчет распределений
            edu_hist = np.histogram(clusters[:len(edu_texts)], bins=n_clusters, density=True)[0]
            jobs_hist = np.histogram(clusters[len(edu_texts):], bins=n_clusters, density=True)[0]
            cluster_match = 1 - jensenshannon(edu_hist, jobs_hist)
        else:
            cluster_match = 0.0  # Если кластеризация невозможна
        
        # Расчет семантического сходства
        semantic_sim = cosine_similarity(
            [np.mean(edu_emb, axis=0)], 
            [np.mean(jobs_emb, axis=0)]
        )[0][0] if len(edu_emb) > 0 and len(jobs_emb) > 0 else 0.0
        
        if semantic_sim < 0.51:
            semantic_sim *= 0.15

        # Итоговая оценка
        optimal = 0.8 * semantic_sim + 0.2 * cluster_match
        
        results = {
            'semantic': round(semantic_sim, 3),
            'cluster': round(cluster_match, 3),
            'optimal': np.clip(round(optimal, 3), 0.0, 1.0)
            }
        
        return [f'{metric} score', results[metric]]
