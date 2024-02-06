import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import FileCallbackHandler
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from loguru import logger

load_dotenv()


class TreeOfThoughts:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    progress = 0
    model = "gpt-3.5-turbo-16k"
    progress_bar = None
    messages = []
    steps = 0
    temperature = 0.7

    def __init__(self):
        if self.api_key == "":
            st.error("Please add your API key to .env file OPENAI_API_KEY=YOUR_API_KEY")
            exit(1)

    def run(self):
        st.title("Chain Of Thoughts")
        # "with" notation
        with st.sidebar:
            option = st.selectbox(
                'Choose your model',
                ('gpt-3.5-turbo-16k', 'gpt-4-32k'))
            self.model = option

            temperature = st.slider(
                'Choose your temperature',
                0.0, 1.0, 0.7
            )
            self.temperature = temperature

            steps = st.selectbox(
                'Choose your steps',
                list(range(2, 200))
            )
            self.steps = steps

        st.caption(f"Using model: {self.model}")

        prompt = st.chat_input("What is your problem you are trying to solve: ")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            self.progress_bar = st.progress(0)
            solution = self.solve(prompt)
            self.progress_bar.empty()
            with st.chat_message("assistant"):
                st.write(solution)

    def solve(self, problem: str):
        self.progress_bar.progress(0, "Solving your problem...")
        # Only certain models support this
        llm = ChatOpenAI(model=self.model, temperature=self.temperature)
        current_timestamp = datetime.timestamp(datetime.now())
        log_file = Path(f"./logs-{current_timestamp}.txt")
        logger.add(Path(log_file), colorize=True, enqueue=True)
        handler = FileCallbackHandler(str(log_file))
        conversation = ConversationChain(llm=llm, callbacks=[handler], verbose=True)
        prompts = []
        files = []
        for file in Path('./prompts').glob('*.txt'):
            if file.is_file():
                files.append(file)
        # Sort files by name
        files.sort(key=lambda x: int(x.stem))
        for index, file in enumerate(files):
            prompt = file.read_text().strip()
            prompt = prompt.replace('<<PROBLEM>>', problem)
            if index == 1 and index == len(files) - 2:
                for i in range(self.steps):
                    prompts.append(prompt)
            else:
                prompts.append(prompt)
        for index, prompt in enumerate(prompts):
            conversation.invoke(prompt)
            self.progress_bar.progress(round((index + 1) / len(prompts) * 100), "Solving your problem...")
        return conversation.memory.chat_memory.messages[-1].content


if __name__ == '__main__':
    chain = TreeOfThoughts()
    chain.run()
