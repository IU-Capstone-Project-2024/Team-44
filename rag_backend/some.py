from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from lang_graph.router import Router

router = Router()

query = "The exploration of Mars has been a long-standing goal of space agencies around the world. With its similarities to Earth, Mars has often been seen as a potential target for future human missions. However, before humans can set foot on the Red Planet, robotic missions are necessary to gather data and pave the way for human exploration. NASA's Perseverance Rover is the latest in a long line of Mars missions. Launched on July 30, 2020, the rover made its dramatic landing in the Jezero Crater on Feb. 18, 2021. The landing site was carefully chosen for its potential to host signs of ancient microbial life. Jezero Crater is believed to have once been a lake, and the rover will search for evidence of past life in the sediments left behind. The Perseverance Rover is equipped with a suite of advanced scientific instruments. These include a drill to collect samples of Martian rock and soil, a camera system to capture high-resolution images, and a miniature helicopter named Ingenuity to test powered flight on Mars. The rover will also test technologies to produce oxygen from the Martian atmosphere, a key step towards future human missions. The mission is expected to last at least one Martian year, or about 687 Earth days. During this time, the rover will traverse the Martian surface, collect and analyze samples, and send data back to Earth. The data gathered by Perseverance will not only advance our understanding of Mars, but also help pave the way for future human missions to the Red Planet."

text_splitter = RecursiveCharacterTextSplitter()
text = text_splitter.create_documents([query])


verdict = router.add_docs(text)
result = router.retrieve(query)

print(verdict)
print(result)
