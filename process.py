# %%
import pandas as pd
from pathlib import Path


# get the latest file from current directory
def pre_process(latest_file: Path = None):

    if latest_file is None:
        current_folder = Path(__file__).resolve().parent
        latest_file = max(current_folder.glob("*.csv"), key=lambda f: f.stat().st_ctime)

    df = pd.read_csv(latest_file, encoding="cp949", sep=",", skiprows=15, header=0)
    df.rename(
        {
            "대지권면적(㎡)": "대지면적",
            "거래금액(만원)": "거래금액",
            "전용면적(㎡)": "전용면적",
        },
        axis="columns",
        inplace=True,
    )

    # print(df.columns)
    # %%
    df["본번"] = df["본번"].astype(int)
    df["대지면적"] = df["대지면적"].astype(float)
    # 만약에 '거래금액' 컬럼의 값에 '        ' 빈칸을 포함하고 있다면 ' ' 빈칸을 제거해준다.
    df["거래금액"] = df["거래금액"].str.replace(" ", "")
    # df['거래금액'] 컬럼은 천 단위 구분자를 제거하고 int형으로 변환
    df["거래금액"] = df["거래금액"].str.replace(",", "").astype(int)

    df["층"] = df["층"].astype(int)

    # df['계약년월'] 컬럼을 strptime을 이용하여 YYYYMM 형식으로 변환
    # df["계약년월"] = pd.to_datetime(df["계약년월"], format="%Y%m")

    df["계약날짜"] = pd.to_datetime(
        (df["계약년월"].astype(str) + df["계약일"].astype(str)), format="%Y%m%d"
    ).dt.strftime("%Y-%m-%d")

    # 만약에 '본번' 컬럼의 값이 241부터 402까지의 값이라면 '양재2동'컬럼에 True를 넣어주고 아니라면 False를 넣어준다.
    df["양재2동"] = df["본번"].between(241, 402)
    # 만약에 '본번' 컬럼의 값이 358부터 391까지의 값이라면 '일구역'컬럼에 True를 넣어주고 아니라면 False를 넣어준다.
    df["일구역"] = df["본번"].between(358, 391)
    df["대지면적평당가격"] = df["거래금액"] / (df["대지면적"] / 3.306)
    df["대지면적평당가격"] = df["대지면적평당가격"].round(-1)
    df["대지면적평당가격"] = df["대지면적평당가격"].astype(int)
    df["updated_at"] = pd.to_datetime("now").strftime("%Y-%m-%d %H:%M:%S")
    # %%
    # df에서 번지, 본번, 부번, 건물명, 전용면적, 대지면적, 계약날짜, 거래금액, 건축년도, 대지면적평당가격, 양재2동, 일구역 컬럼만 가져온다.
    df = df.loc[
        :,
        [
            "번지",
            "본번",
            "부번",
            "건물명",
            "층",
            "전용면적",
            "대지면적",
            "계약날짜",
            "거래금액",
            "건축년도",
            "대지면적평당가격",
            "양재2동",
            "일구역",
            "updated_at",
        ],
    ]
    # %%
    # 전체 df에서 '양재2동'컬럼이 True인 값만 가져온다.
    df = df[df["양재2동"]]
    df = df.sort_values(by="계약날짜", ascending=False)
    # 일구역에 해당하는 데이터만 가져온다.
    df1 = df[df["일구역"]]

    # %%
    return df1.head(20), df.head(20)


if __name__ == "__main__":
    df1, df = pre_process()
    print(df1)
    print(df)
