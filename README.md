🚀 AI Document Analyst (RAG)
Un chatbot IA full-stack qui répond de manière intelligente et contextuelle à des questions complexes sur vos documents privés.

📜 Aperçu
Ce projet est un chatbot IA full-stack qui va au-delà d'une simple conversation. Grâce à un pipeline de Retrieval-Augmented Generation (RAG), il permet à l'API Gemini Pro de Google d'analyser en profondeur le contenu de documents fournis par l'utilisateur (.pdf, .docx, .txt) et de fournir des réponses précises et sourcées.

✨ Fonctionnalités Clés
Upload Multi-fichiers : Accepte plusieurs documents de formats variés (PDF, DOCX, TXT).

Traitement de Texte Intelligent : Divise les documents en "chunks" optimisés pour le traitement par le LLM.

Base de Données Vectorielle : Crée des embeddings des chunks de texte et les stocke pour une recherche sémantique rapide.

Pipeline RAG : Pour chaque question, le système retrouve les passages les plus pertinents dans les documents et les fournit au LLM comme contexte, garantissant des réponses factuelles et précises.

Interface Utilisateur Interactive : Une interface simple et intuitive construite avec Streamlit.

🛠️ Architecture et Stack Technique
Application : Python, Streamlit

IA / ML : Google Gemini Pro, LangChain (pour le pipeline RAG), Sentence Transformers (pour les embeddings)

Base de Données Vectorielle : FAISS (ou ChromaDB)

Déploiement : Streamlit Community Cloud, Git, GitHub

⚙️ Installation et Lancement
Pour lancer ce projet localement, suivez ces étapes :

Clonez le repository :

Bash

git clone https://github.com/yahias29/ai-chatbot.git
cd ai-chatbot
Créez un environnement virtuel et installez les dépendances :

Bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configurez les variables d'environnement :

Créez un fichier .env à la racine.

Ajoutez votre clé API Google :

GOOGLE_API_KEY="VOTRE_CLÉ_API_GOOGLE"
Lancez l'application Streamlit :

Bash

streamlit run app.py
🧠 Défis et Apprentissages
Le défi principal dans un projet RAG est d'assurer la pertinence et la précision des réponses tout en minimisant les hallucinations. J'ai beaucoup appris sur :

Le "Chunking" Stratégique : L'importance de bien découper le texte pour préserver le contexte sémantique.

L'Optimisation des Prompts : La rédaction de prompts qui forcent le LLM à se baser uniquement sur le contexte fourni par les documents, en lui demandant de répondre "Je ne sais pas" si l'information n'est pas présente.

La Gestion de la Mémoire Conversationnelle : Permettre au chatbot de se souvenir des questions précédentes pour des conversations plus fluides.
