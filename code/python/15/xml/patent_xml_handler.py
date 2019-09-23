from bs4 import BeautifulSoup

def get_patent_info(pat_document):
    soup = BeautifulSoup(pat_document, "lxml")  # xml parser 호출
    invention_title = soup.find("invention-title").get_text()
    publication_reference_tag = soup.find("publication-reference")
    p_document_id_tag = publication_reference_tag.find("document-id")
    p_doc_number = p_document_id_tag.find("doc-number").get_text()
    p_date = p_document_id_tag.find("date").get_text()

    return [invention_title, p_doc_number, p_date]

f = open("./ipa110106.XML", "r")
full_contents_list = f.readlines()
f.close()

target_idx_list = []
for idx, line in enumerate(full_contents_list):
    if line.strip().startswith('<?xml version="1.0"'):
        target_idx_list.append(idx)
print(target_idx_list)

pat_document_list = []
for idx in range(len(target_idx_list)-1):
    pat_document = "\n".join(full_contents_list[
        target_idx_list[idx]: target_idx_list[idx+1]])
    pat_document_list.append(pat_document)

f = open("pat_info.csv", "w")
for pat_document in pat_document_list:
    line = "\t".join(get_patent_info(pat_document))
    print(line)
    f.write(line)
f.close()
