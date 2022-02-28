import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import asyncio
from tortoise import Tortoise
from model import SampleNFT, Trait


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
    await SampleNFT.create(
        name="NFT 이름",
        description="NFT 설명",
        image="NFT 이미지 소스 URL",
        external_url="NFT 외부 URL",
        attributes=[Trait(display_type="level", trait_type="Level", value=1000)],
    )
    print("생성 완료")


asyncio.run(main())
