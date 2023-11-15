import openai
import logging
from . import BaseStrategy

logger = logging.getLogger(__name__)


class SimplePromptStrategy(BaseStrategy):
    def get_prompt(self, question, answers):
        """Return the prompt for the question and answers"""
        return f"""
        {question} Give Response as a single letter from options that answers this qu.
        # Options 
        {answers}
        """

    def determine_answer(self, qu, answers):
        """Use ChatGPT to solve qu and return answer from answers"""
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct", prompt=self.get_prompt(qu, answers), temperature=1.0
        )
        logger.info(response)
        answer = response.choices[0].text
        answer = answer.strip("\n").strip(" ")[0]
        if answer not in ["A", "B", "C", "D"]:
            raise Exception("Wrong Choice! Investigate ChatGPT response...")
        return answer