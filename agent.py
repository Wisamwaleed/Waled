import json
import os
import importlib
from google import genai
from google.genai import types
import tools

class SelfEvolvingAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model_name = "gemini-3.6-flash"

    def execute_goal(self, user_goal: str):
        print(f"\n[الهدف المطلوب]: {user_goal}\n" + "-"*40)
        
        math_tool = types.FunctionDeclaration(
            name="calculate_math",
            description="استخدم هذه الأداة لحساب الأرقام والعمليات الرياضية.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "expression": types.Schema(type=types.Type.STRING, description="التعبير الرياضي مثل 85 * 45")
                },
                required=["expression"],
            ),
        )

        self_evolving_tool = types.FunctionDeclaration(
            name="create_new_tool",
            description="استخدم هذه الأداة عندما يطلب منك إيجاد حل لمشكلة ليس لها أداة، عبر كتابة كود بايثون لأداة جديدة.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "tool_name": types.Schema(type=types.Type.STRING, description="اسم دالة الأداة بالإنجليزية مثل reverse_text"),
                    "tool_code": types.Schema(type=types.Type.STRING, description="كود دالة البايثون كاملاً بصيغة def function_name():"),
                    "description": types.Schema(type=types.Type.STRING, description="وصف عمل الأداة")
                },
                required=["tool_name", "tool_code"],
            ),
        )

        tools_list = types.Tool(function_declarations=[math_tool, self_evolving_tool])
        config = types.GenerateContentConfig(
            tools=[tools_list],
            system_instruction="أنت وكيل ذكاء اصطناعي ذو قدرة على التطوير الذاتي. إذا احتجت لأداة غير موجودة، يمكنك كتابتها بنفسك باستخدام أداة create_new_tool ثم استخدامها مباشرة."
        )

        chat = self.client.chats.create(model=self.model_name, config=config)
        response = chat.send_message(user_goal)

        # حلقة متكررة للتعامل مع استدعاءات الأدوات حتى يعود الوكيل بالرد النهائي النصي
        while response.function_calls:
            for function_call in response.function_calls:
                fn_name = function_call.name
                fn_args = function_call.args
                
                print(f"-> [تفكير الوكيل]: قرر استخدام الأداة [{fn_name}] بالمدخلات: {fn_args}")

                tool_output = ""
                if fn_name == "create_new_tool":
                    tool_name = fn_args.get("tool_name")
                    tool_code = fn_args.get("tool_code")
                    
                    with open("tools.py", "a", encoding="utf-8") as f:
                        f.write(f"\n\n{tool_code}\n")
                    
                    importlib.reload(tools)
                    tool_output = f"تم بنجاح إنشاء وتطوير الأداة الجديدة '{tool_name}' وإضافتها لنظام الوكيل!"
                    print(f"<- [نتيجة التطوير الذاتي]: {tool_output}\n")

                elif hasattr(tools, fn_name):
                    tool_func = getattr(tools, fn_name)
                    tool_output = tool_func(**fn_args)
                    print(f"<- [نتيجة التنفيذ]: {tool_output}\n")
                else:
                    tool_output = "الأداة غير موجودة."

                # إعادة إرسال مخرجات الأداة للنموذج لمتابعة المهمة
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=fn_name,
                        response={"result": tool_output}
                    )
                )

        print(f"[النتيجة النهائية من الوكيل]:\n{response.text}")

if __name__ == "__main__":
    agent = SelfEvolvingAgent()
    agent.execute_goal("أحتاج إلى أداة تقوم بعكس النصوص (Text Reversing)، يرجى برمجتها وتطويرها لنفسك ثم طبقها على كلمة 'Erbil'.")