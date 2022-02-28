import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import asyncio
from tortoise import Tortoise
from model import SampleNFT


async def main():
    print("[ Create NFT metadata ]")
    print("메타데이터 데이터베이스에 연결중입니다...")
    try:
        await Tortoise.init(
            db_url="sqlite://data/db.sqlite3", modules={"models": ["model"]}
        )
        await Tortoise.generate_schemas()
        print("메타데이터 데이터베이스에 연결되었습니다.\n")
    except Exception as error:
        print("아래 오류로 인해 메타데이터 데이터베이스 연결에 실패했습니다\n\n")
        print(error)
        sys.exit()

    print("메타데이터를 콘솔에서 수동으로 추가할 수 있습니다.")
    print("추가하고 싶지 않은 항목이 있다면 [Enter] 키를 눌러 패스하세요")
    print("이 앱을 종료하려면 콘솔 창을 닫거나 [Ctrl]+[C]를 누르시면 됩니다.")
    print("* Attributes 추가는 지원하지 않습니다.")
    print("아래에서 수동으로 입력해 메타데이터를 추가하세요.\n\n\n")
    print()
    count = 0
    while True:
        print(f"{count}번째 NFT에 메타데이터를 추가합니다.")
        name = input("name:")
        description = input("description:")
        image = input("image:")
        external_url = input("external_url:")
        await SampleNFT.create(
            name=name,
            description=description,
            image=image,
            external_url=external_url,
        )
        print(f"✅ {count}번째 NFT 메타데이터를 추가했습니다.\n")
        count += 1


asyncio.run(main())
