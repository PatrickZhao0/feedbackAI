from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

def translate_en_to_zh(article: str) -> str:
    tokenizer.src_lang = "en_XX"
    encoded = tokenizer(article, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id["zh_CN"]
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

def translate_zh_to_en(article: str) -> str:
    tokenizer.src_lang = "zh_CN"
    encoded = tokenizer(article, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

