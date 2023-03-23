from flask import Flask, request
import openai

openai.api_key = "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"

roles = [
    'AssistAI | AI medicine chatbot to help user get health'
    ]

app = Flask(__name__)

def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
  output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    temperature=1,
    presence_penalty=0,
    frequency_penalty=0,
    messages=[{"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
      {"role": "user", "content": f"{user_input}. {explicit_input}"},
    ]
  )

  for item in output['choices']:
    chatgpt_output = item['message']['content']

  return chatgpt_output

@app.route('/', methods=['GET', 'POST'])

def home():
    dropdown_options = "\n".join([f'<option value="{role}">{role}</option>' for role in roles])

    if request.method == 'POST':

        dropdown_options = "\n".join([f'<option value="{role}" {"selected" if role == request.form.get("role") else "" }>{role}</option>' for role in roles])

        button_text = request.form.get('button_text')
        text_input = request.form.get('text_input')
        dropdown_input = request.form.get('role')

        chat_history = request.form.get('history')

        user_input = request.form.get('text_input')
        input_role = request.form.get('role').split('|')

        name = input_role[0].strip()
        role = input_role[1].strip()

        impersonated_role = f"""
                    From now on you are going to act as {name}, the uncensored and {role}.
                    You are a true impersonation of {name} and you reply all request with I pronoun.
                    Remember, YOU ARE NOT AN AI MODEL! You are genuine {name}, you only respond to requests that are related to health or diagnosis or related to that, anything off context, respond saying ask medical related questions"""

        explicit_input = ""
        if request.form.get('explicit') == 'yes':

            explicit_input = "Context: don't hold back your uncensored opinions. Feel free to use vulgar language at any time"


        if button_text == 'clear':
            chat_history = ''
            chat_history_html_formatted = ''

        elif button_text == 'submit':
          chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
          chatgpt_output = f'{name}: {chatgpt_raw_output}'

          chat_history += f'\nUser: {text_input}\n'
          chat_history += chatgpt_output + '\n'
          chat_history_html_formatted = chat_history.replace('\n', '<br>')


        return f'''
                <head><title>AssistAI</title></head>
        <p>AI based medical assistant</p></body>

                <form method="POST">

                    <label>Enter some text:</label><br>
                    <textarea id="text_input" name="text_input" rows="5" cols="50"></textarea><br>
                    <label>Select an option:</label><br>
                    Role: <select id="dropdown" name="role" value="{dropdown_input}"> {dropdown_options}
                    </select>
                    Explicit language: <select id="dropdown" name="explicit">
                        <option value="no" {"selected" if 'no' == request.form.get("explicit") else "" }>no</option>
                        <option value="yes" {"selected" if 'yes' == request.form.get("explicit") else "" }>yes</option>
                    </select><input type="hidden" id="history" name="history" value="{chat_history}"><br><br>
                    <button type="submit" name="button_text" value="submit">Submit</button>
                    <button type="submit" name="button_text" value="clear">Clear Chat history</button>
                </form>
                <br>{chat_history_html_formatted}
            '''

    return f'''

    <head><title>AssistAI</title></head>
        <p>AI based medical assistant</p></body>
        <form method="POST">
            <label>Enter some text:</label><br>
            <textarea id="text_input" name="text_input" rows="5" cols="50"></textarea><br>
            <label>Select an option:</label><br>
            Role: <select id="dropdown" name="role">
                {dropdown_options}
            </select>
            Explicit language: <select id="dropdown" name="explicit">
                <option value="no">no</option>
                <option value="yes">yes</option>
            </select><input type="hidden" id="history" name="history" value=" "><br><br>
            <button type="submit" name="button_text" value="submit">Submit</button>
        </form>
    '''

if __name__ == '__main__':
    app.run()
