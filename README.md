# Anti-Social-Activities-Detection

Social media has a daily impression on our life, with protests and rebellious movements now shifting online, it possesses great power of influence and is often exploited to spread a hatred propaganda and anti-social activities. Now, laws been made to regard social media platforms as publishers, there is a need for a robust system to detect and eradicate these anti-social activities. The subtle design and format of multimodal signals provide inherent challenge to learn from the signals. The researchers have used unimodal models but they failed to address the context of different modalities combined together, therefore a true multimodal system is required. Some researchers have started working on multimodal signal analysis but they majorly focus on binary classification. This extends it to multi-class classification and develop a system using Artificial Intelligence techniques to detect anti-social activities in multi-modal signals whether it is textual, audio, visual or combination of one or two. On top of that it is deployed for real-time data analysis of one such social media platform (Twitter) in form of a dashboard. Different datasets were merged and manually annotated for Benign Confounders which is a crucial element when understanding the complex relationship in the multimodal signals.Finally, managed to achieve better performance than unimodal models with accuracy of around 90% for textual and audio signals; accuracy of around 70% for visual signals like images and accuracy of around 90% for visual signals like videos.

### Google Colab and Google Drive were used as the Development Enviroment

Interaction is in the form of a Dashboard (Script: [Link](https://github.com/avioberoi/Anti-Social-Activities-Detection/blob/main/Dashboard.ipynb)). Following the instructions, the server on Remote Machine in Google Colab can be exposed to the internet with help of ngrok and use of dashboard can visualised in the form of a Flask Web App.

### Datasets

The model was implemented and tested on datasets like [Facebook Hateful Memes Dataset](https://hatefulmemeschallenge.com), [MMHS150K Dataset](https://gombru.github.io/2019/10/09/MMHS/) for classification of visual data like images into Racist, Sexist, Hate and Non-Hate; Rose Lab [NTU CCTV-Fights Dataset](https://rose1.ntu.edu.sg/dataset/cctvFights/), [Hockey Fight Detection Dataset](https://academictorrents.com/details/38d9ed996a5a75a039b84cf8a137be794e7cee89) for classification of visual data like videos into Hateful and Non-Hateful; Customized and self-produced dataset for classification of audio data into Hateful and Non-Hateful; Real-Time Twitter data for classification of Textual into Hateful, Offensive and Non-Hateful.

### MMF

Utilization of the [mmf](https://github.com/facebookresearch/mmf) framework for building deep learning architectures and baseline models for the task of detecting anti-social activities in multimodal signals has been done. Architectures like a CNN (Convolutional Neural Network), LSTM (Long-Short-Term-Memory) built on top of baseline models like MMBT (Multi-Modal-Bi-Transformers), Visual BERT (Bidirectional Encoder Representations from Transformers), ViLBERT (Vision and Language BERT), etc.

### Twitter Dashboard

Extraction and processing of real-time twitter data with help of [Twitter API](https://developer.twitter.com/en/docs/twitter-api) and showing it in graphical form with sentiment analysis and frequency distribution.

