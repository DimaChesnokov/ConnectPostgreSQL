from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Данные для подключения
host = "povt-cluster.tstu.tver.ru"
port = 5432
user = "mpi"
password = "135a1"
database = "db_housing"

# Подключение к базе данных
try:
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}?client_encoding=utf8")
    print("Подключение успешно")
except Exception as e:
    print("Ошибка подключения:", e)
    exit()

# Проверка наличия таблицы и выполнения запроса
try:
    query = 'SELECT * FROM "Nashville_Housing" LIMIT 1000'  # Ограничиваем выборку
    df = pd.read_sql_query(query, engine)
    print("Данные успешно загружены в DataFrame")
    print("Колонки в таблице:", df.columns.tolist())  # Выводим список колонок для проверки
    print(df.head())

    # Фильтрация: выбор только важных признаков
    important_columns = ["landuse", "soldasvacant", "saleprice", "acreage", "yearbuilt"]
    filtered_df = df[important_columns]
    print("Отфильтрованный DataFrame:")
    print(filtered_df.head())

    # Одномерный анализ: Построение гистограмм
    for feature in ["saleprice", "acreage"]:  # Количественные признаки
        if feature in filtered_df.columns:
            plt.figure(figsize=(8, 5))
            plt.hist(filtered_df[feature].dropna(), bins=30, edgecolor="k", alpha=0.7)
            plt.title(f"Распределение признака: {feature}")
            plt.xlabel("Площадь участка (акры)" if feature == "acreage" else feature)
            plt.ylabel("Частота")

            # Форматирование оси X в формате целых чисел для saleprice
            if feature == "saleprice":
                ax = plt.gca()
                ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))  # Формат в виде тысяч

            plt.grid(True)
            plt.show()
        else:
            print(f"Признак '{feature}' не найден в данных.")

    # Многомерный анализ: Построение графиков

    # График 1: Зависимость saleprice от acreage без категорий SINGLE FAMILY
    filtered_data_no_single_family = filtered_df[filtered_df["landuse"] != "SINGLE FAMILY"]

    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=filtered_data_no_single_family,
        x="acreage",
        y="saleprice",
        hue="landuse",
        alpha=0.7
    )
    plt.title("Зависимость saleprice от acreage без категорий SINGLE FAMILY")
    plt.xlabel("Площадь участка (акры)")
    plt.ylabel("Цена продажи")
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))  # Форматирование оси Y
    plt.grid(True)
    plt.legend(title="Тип использования земли")
    plt.show()

    # График 2: Распределение saleprice по yearbuilt и soldasvacant
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=filtered_df, x="yearbuilt", y="saleprice", hue="soldasvacant")
    plt.title("Распределение saleprice по yearbuilt и soldasvacant")
    plt.xlabel("Год постройки")
    plt.ylabel("Цена продажи")
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))  # Форматирование оси Y
    plt.xticks(rotation=45)
    plt.legend(title="Продано как пустой участок")
    plt.grid(True)
    plt.show()

except Exception as e:
    print("Ошибка выполнения запроса:", e)
