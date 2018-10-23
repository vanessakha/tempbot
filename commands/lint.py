from yapf.yapflib.yapf_api import FormatCode
import re


async def lint(client, message, params):
    if(re.match("(?<=(```py\n))(.*)(?=(\n```))", params)):
        code = re.sub("(?<=(```py\n))(.*)(?=(\n```))", '',
                      params)  # removes code header tags
        # uses yapf to format w/ pep8 linter
        formatted = FormatCode(code, style_config='pep8')
        await client.send_message("```py\n" + formatted + "\n```")
    else:
        # keep the language SPICY
        await client.send_message(message.channel, "Invalid code, buckeroo!")
