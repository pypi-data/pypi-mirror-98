class preprocessing:
    def __init__(self, input_string):
        self.input_string = input_string

    def punctuation(self):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        my_str = self.input_string.lower()
        no_punct = ""
        for char in my_str:
            if char not in punctuations:
                no_punct = no_punct + char
        return no_punct

    def tokenization(self):
        processed_text = self.punctuation().split()
        return processed_text


    def stop_words(self):
        filtered_list = []
        stopwords =["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                 "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                 "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                 "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                 "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                 "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                 "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                 "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                 "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                 "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                 "now"]

        tokens = self.tokenization()
        for words in tokens:
            if words not in stopwords:
                filtered_list.append(words)
        return filtered_list


    def bag_of_words(self):
        word2count = {}
        words = self.stop_words()
        for word in words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
        return word2count

    def split(self):
        pass









# def tokenization(input_string):
#     processed_text = input_string.split()
#     return processed_text
#
# filtered_list = []
# stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
# def stop_words(input_string):
#     tokens = tokenization(input_string)
#     for words in tokens:
#         if words not in stopwords:
#             filtered_list.append(words)
#     return filtered_list


