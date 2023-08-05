def search_vowels(word:str) -> set: 
	"""返回在单词word中找到的所有元音"""
	vowels = set('aeiou')
	return vowels.intersection(set(word))

def search_letters(phrase:str, letters:str='aeiou') -> set:
  	"""返回一个letters和phrase的交集（集合）"""
  	return set(letters).intersection(set(phrase))
