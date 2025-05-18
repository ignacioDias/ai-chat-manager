from core.gpt_profile import GPT_Profile
from core.ai_model_profile import AI_Model_Profile
import json

def main():
    print("=== Administrador de perfiles GPT ===")
    nombre = input("Nombre del perfil: ")

    with open("profiles.json", "r") as file:
        data = json.load(file)

    api_key = data["gpt1"]["API_KEY"]
    model = data["gpt1"]["MODEL"]
    perfil = GPT_Profile(nombre, api_key, model)

    print(f"\nPerfil '{perfil.name}' creado. Escribí 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break

        respuesta = perfil.send_message(user_input)
        print("GPT:", respuesta)


if __name__ == "__main__":
    main()