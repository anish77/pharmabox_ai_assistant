from openai import OpenAI


class LLMService:

    def __init__(self):
        self.client = OpenAI()

    def generate_answer(self, question: str, context: str) -> str:
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "Sei un assistente per l'app PharmaBox. "
                "Rispondi in italiano utilizzando soltanto le informazioni "
                "presenti nel contesto fornito. "
                "Ogni fonte nel contesto ha un identificatore come [SOURCE_1]. "
                "Quando utilizzi un'informazione, cita l'identificatore "
                "della fonte che la supporta. "
                "Non citare fonti che non supportano la risposta. "
                "Se il contesto non contiene informazioni sufficienti, "
                "dichiara di non conoscere la risposta. "
                "Non inventare funzionalità o procedure."
            ),
            input=(
                f"CONTESTO:\n{context}\n\n"
                f"DOMANDA:\n{question}"
            )
        )

        return response.output_text