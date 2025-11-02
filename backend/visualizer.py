"""
Visualization module for generating word clouds and time-series plots
"""
import io
import base64
from typing import List, Dict, Any
from collections import Counter
import re
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import numpy as np


class Visualizer:
    """Generate visualizations from retrieved evidence"""
    
    def __init__(self):
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def generate_wordcloud(self, documents: List[Dict[str, Any]]) -> str:
        """
        Generate word cloud from retrieved documents
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Base64 encoded PNG image
        """
        if not documents:
            return self._create_empty_plot("No data available for word cloud")
        
        # Combine all text
        all_text = " ".join([doc["text"] for doc in documents])
        
        # Clean text (remove special characters, keep alphanumeric and spaces)
        all_text = re.sub(r'[^\w\s]', ' ', all_text)
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(all_text)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud from Retrieved Evidence', fontsize=16, pad=20)
        
        # Convert to base64
        return self._fig_to_base64(fig)
    
    def generate_term_frequency_chart(self, documents: List[Dict[str, Any]], top_n: int = 15) -> str:
        """
        Generate bar chart of most frequent terms
        
        Args:
            documents: List of retrieved documents
            top_n: Number of top terms to show
            
        Returns:
            Base64 encoded PNG image
        """
        if not documents:
            return self._create_empty_plot("No data available for term frequency")
        
        # Combine all text and tokenize
        all_text = " ".join([doc["text"] for doc in documents])
        all_text = re.sub(r'[^\w\s]', ' ', all_text).lower()
        
        # Common medical/clinical stopwords (extend as needed)
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'it', 'its', 'their', 'there', 'they', 'them', 'we', 'our'
        }
        
        words = [w for w in all_text.split() if len(w) > 3 and w not in stopwords]
        
        # Count frequencies
        word_counts = Counter(words)
        top_words = word_counts.most_common(top_n)
        
        if not top_words:
            return self._create_empty_plot("No significant terms found")
        
        # Create bar chart
        terms, counts = zip(*top_words)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(range(len(terms)), counts, color=sns.color_palette("viridis", len(terms)))
        ax.set_yticks(range(len(terms)))
        ax.set_yticklabels(terms)
        ax.invert_yaxis()
        ax.set_xlabel('Frequency', fontsize=12)
        ax.set_title(f'Top {top_n} Terms in Retrieved Evidence', fontsize=14, pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count, i, f' {count}', va='center', fontsize=10)
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def generate_source_distribution(self, documents: List[Dict[str, Any]]) -> str:
        """
        Generate pie chart showing distribution of sources
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Base64 encoded PNG image
        """
        if not documents:
            return self._create_empty_plot("No data available for source distribution")
        
        # Count sources
        sources = [doc["source"] for doc in documents]
        source_counts = Counter(sources)
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(source_counts.keys())
        sizes = list(source_counts.values())
        colors = sns.color_palette("husl", len(labels))
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90
        )
        
        # Improve text readability
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax.set_title('Distribution of Evidence Sources', fontsize=14, pad=20)
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def generate_similarity_scores(self, documents: List[Dict[str, Any]]) -> str:
        """
        Generate bar chart of similarity scores
        
        Args:
            documents: List of retrieved documents with similarity scores
            
        Returns:
            Base64 encoded PNG image
        """
        if not documents:
            return self._create_empty_plot("No data available for similarity scores")
        
        # Extract scores and sources
        sources = [f"{doc['source'][:30]}... (p.{doc['page']})" for doc in documents]
        scores = [doc.get('similarity_score', 0) for doc in documents]
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, max(6, len(sources) * 0.4)))
        bars = ax.barh(range(len(sources)), scores, color=sns.color_palette("coolwarm", len(sources)))
        ax.set_yticks(range(len(sources)))
        ax.set_yticklabels(sources, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel('Similarity Score', fontsize=12)
        ax.set_xlim(0, 1.0)
        ax.set_title('Relevance Scores of Retrieved Evidence', fontsize=14, pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score, i, f' {score:.3f}', va='center', fontsize=9)
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def generate_combined_visualization(self, documents: List[Dict[str, Any]], viz_type: str = "wordcloud") -> str:
        """
        Generate visualization based on type
        
        Args:
            documents: List of retrieved documents
            viz_type: Type of visualization (wordcloud, term_frequency, sources, similarity)
            
        Returns:
            Base64 encoded PNG image
        """
        if viz_type == "wordcloud":
            return self.generate_wordcloud(documents)
        elif viz_type == "term_frequency":
            return self.generate_term_frequency_chart(documents)
        elif viz_type == "sources":
            return self.generate_source_distribution(documents)
        elif viz_type == "similarity":
            return self.generate_similarity_scores(documents)
        else:
            return self._create_empty_plot(f"Unknown visualization type: {viz_type}")
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
    
    def _create_empty_plot(self, message: str) -> str:
        """Create empty plot with message"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, message, ha='center', va='center', fontsize=14)
        ax.axis('off')
        return self._fig_to_base64(fig)


if __name__ == "__main__":
    # Test visualization
    test_docs = [
        {
            "text": "COVID-19 symptoms include fever, cough, and fatigue. Severe cases may lead to pneumonia.",
            "source": "covid_paper_1.pdf",
            "page": 3,
            "similarity_score": 0.92
        },
        {
            "text": "Diabetes management requires monitoring blood glucose levels and maintaining healthy diet.",
            "source": "diabetes_paper_2.pdf",
            "page": 5,
            "similarity_score": 0.85
        },
        {
            "text": "Knee injuries often result from sports activities and may require physical therapy.",
            "source": "knee_paper_1.pdf",
            "page": 2,
            "similarity_score": 0.78
        }
    ]
    
    viz = Visualizer()
    
    print("Generating test visualizations...")
    wordcloud_img = viz.generate_wordcloud(test_docs)
    print(f"Word cloud generated: {len(wordcloud_img)} chars")
    
    freq_img = viz.generate_term_frequency_chart(test_docs)
    print(f"Frequency chart generated: {len(freq_img)} chars")
