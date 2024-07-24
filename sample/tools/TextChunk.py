from crewai_tools import BaseTool

class TextChunkTool(BaseTool):
    name: str = "Text Chunk tool"
    description: str = "This tool is used to chunk text if a given LLM prompt exceeds its token limit."

    def _run(text):
        chunks = [[]]
        chunk_total_words = 0

        sentences = nlp(text)

        for sentence in sentences.sents:
            chunk_total_words += len(sentence.text.split(" "))

            if chunk_total_words > 2700:
                chunks.append([])
                chunk_total_words = len(sentence.text.split(" "))

            chunks[len(chunks) - 1].append(sentence.text)

        return chunks
