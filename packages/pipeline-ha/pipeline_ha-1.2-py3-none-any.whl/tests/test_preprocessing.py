from pipeline_ha import preprocessing_func
def test():
    obj =preprocessing_func.preprocessing("i am Himanshu ?!@ is Aditya")
    # obj.stop_words() == ['Himanshu', 'Aditya']
    obj.bag_of_words == [1,1]

# def test_tokenization():
#     assert preprocessing_func.tokenization("the given data") == ['the', 'given', 'data']
#
# def test_stop_words():
#     assert preprocessing_func.stop_words("the given data") == ['given', 'data']

