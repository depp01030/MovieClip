import asyncio

# === 要跑哪個腳本就取消註解那一段 ===
from app.movieclip.run import run as movieclip_run
# from app.another_task.run import run as another_task_run

#%%
'''
錄製指令
playwright codegen  

'''

async def main():
    # await another_task_run()
    await movieclip_run()  # 目前只跑 movieclip

if __name__ == "__main__":
    asyncio.run(main())
