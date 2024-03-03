import pandas as pd
from BackEnd.rank_predictor import pvr


def finalList(mainrank, perc, category, state, gender, pwd, limit, advrank):
    dataset = pd.read_csv('BackEnd/cleaned.csv')

    dataset["Closing Rank"] = pd.to_numeric(dataset["Closing Rank"], errors="coerce").astype("Int64")
    # The algorithm showed some anomaly when %tile was 100.
    # Hence, the following condition.
    p_adv = pd.DataFrame()
    p_mains = pd.DataFrame()
    if mainrank == '-1':
        rank = float(pvr(perc, pwd, category))
    else:
        rank = mainrank

    if pwd == 'YES':
        if gender == 'M':
            catg = category + '-PwD'
            if rank > 0:
                p_mains = dataset[
                    (dataset['Closing Rank'] >= rank) & (
                            (dataset['Category'] == catg) | (dataset['Category'] == 'OPEN-PwD')) & (
                            dataset['Gender'] == 'Gender-Neutral') & (dataset['IIT'] == 0)]
            if advrank > 0:
                p_adv = dataset[
                    (dataset['Closing Rank'] >= advrank) & (
                            (dataset['Category'] == catg) | (dataset['Category'] == 'OPEN-PwD')) & (
                            dataset['Gender'] == 'Gender-Neutral') & (dataset['IIT'] == 1)]
        else:
            catg = category + '-PwD'
            if rank > 0:
                p_mains = dataset[
                    (dataset['Closing Rank'] >= rank) & (
                            (dataset['Category'] == catg) | (dataset['Category'] == 'OPEN-PwD')) & (
                            dataset['IIT'] == 0)]
            if advrank > 0:
                p_adv = dataset[
                    (dataset['Closing Rank'] >= advrank) & (
                            (dataset['Category'] == catg) | (dataset['Category'] == 'OPEN-PwD')) & (
                            dataset['IIT'] == 1)]
    else:
        if gender == 'M':
            if rank > 0:
                p_mains = dataset[
                    (dataset['Closing Rank'] >= rank) & (
                            (dataset['Category'] == category) | (dataset['Category'] == 'OPEN')) & (
                            dataset['Gender'] == 'Gender-Neutral') & (dataset['IIT'] == 0)]
            if advrank > 0:
                p_adv = dataset[
                    (dataset['Closing Rank'] >= advrank) & (
                            (dataset['Category'] == category) | (dataset['Category'] == 'OPEN')) & (
                            dataset['Gender'] == 'Gender-Neutral') & (dataset['IIT'] == 1)]
        else:
            if rank > 0:
                p_mains = dataset[
                    (dataset['Closing Rank'] >= rank) & (
                            (dataset['Category'] == category) | (dataset['Category'] == 'OPEN')) & (
                            dataset['IIT'] == 0)]
            if advrank > 0:
                p_adv = dataset[
                    (dataset['Closing Rank'] >= advrank) & (
                            (dataset['Category'] == category) | (dataset['Category'] == 'OPEN')) & (
                            dataset['IIT'] == 1)]

    if not p_adv.empty and (not p_mains.empty):
        p = pd.concat([p_adv, p_mains])
    elif not p_mains.empty:
        p = p_mains
    else:
        p = p_adv

    v = []
    for i in p.index:
        if p['State'][i] == state:
            if p['Quota'][i] != 'HS':
                v.append(i)
        elif (p['Quota'][i] != 'OS') and (p['Quota'][i] != 'AI'):
            v.append(i)

    q = p.drop(index=v)
    if q.shape[0] > 0:
        q = q.sort_values(by='Closing Rank')
        q = q[0:limit]
        x = q.drop(['Unnamed: 0', 'index', 'Category', 'Opening Rank', 'IIT', 'Round'], axis=1).drop_duplicates()
        x.reset_index(inplace=True, drop=True)
        x.index = x.index + 1
        return x
    else:
        return pd.DataFrame()


# print(finalList(403, 69.3, 'GEN', 'Rajasthan', 'M', 'NO', 10, 562).to_json())
