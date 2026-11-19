#!/usr/bin/env python3
"""키워드 검색 결과(keyword_rows.tsv)를 archive_index.json 에 병합한다.

- 웹메일 검색(s_word)으로 찾은 결과만 담는다 (1년치 전수 수집은 아직 진행 중).
- 같은 메일이 두 번 들어가지 않도록 (mailbox, mf_no) 로 중복 제거하고, 키워드는 tags 에 합친다.
- date 는 PC 목록의 "YY-MM-DD HH:MM" → "YYYY-MM-DD HH:MM".
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, "archive_index.json")
TSV = os.path.join(HERE, "keyword_rows.tsv")


def conv_date(s):
    s = (s or "").strip()
    if len(s) >= 8 and s[2] == "-" and s[5] == "-":
        return "20" + s
    return s


def main():
    with open(IDX, encoding="utf-8") as f:
        idx = json.load(f)
    mails = idx.get("mails") or []
    seen = {(m.get("mailbox") or "inbox") + ":" + str(m.get("mf_no")): m for m in mails}

    added = updated = 0
    with open(TSV, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            box, mf, date, sender, subject, tag = [c.strip() for c in line.split("\t")]
            key = box + ":" + mf
            if key in seen:
                m = seen[key]
                tags = set(m.get("tags") or [])
                tags.add(tag)
                m["tags"] = sorted(tags)
                updated += 1
                continue
            m = {
                "mailbox": box,
                "mf_no": mf,
                "date": conv_date(date),
                "sender": sender,
                "senderEmail": "",
                "subject": subject,
                "tags": [tag],
            }
            mails.append(m)
            seen[key] = m
            added += 1

    mails.sort(key=lambda m: (m.get("date") or ""), reverse=True)
    idx["mails"] = mails
    co = idx.setdefault("coverage", {})
    inbox = [m for m in mails if (m.get("mailbox") or "inbox") == "inbox"]
    sent = [m for m in mails if m.get("mailbox") == "sent"]
    co["inbox"] = {
        "indexed": len(inbox),
        "total": 8397,
        "note": "키워드 검색(근태·조합원 등) 결과 + 최근 분석분만 색인. 1년치 전수 수집은 진행 중.",
    }
    co["sent"] = {
        "indexed": len(sent),
        "total": 720,
        "note": "보낸편지함 일부(2026-06-29~11-19) + 키워드 검색(정례회의·사장단) 결과.",
    }
    idx["note"] = ("받은편지함 8,397건 전체를 한 번에 받아올 수 없어(웹메일 목록 84페이지 · 15~100건 단위) "
                   "지금은 ① 보낸편지함 196건 ② 최근 받은메일 분석분 ③ 주요 키워드(근태·조합원·정례회의·사장단) "
                   "검색 결과를 색인했다. 키워드로 걸러낸 항목에는 tags 가 붙어 대시보드 검색에 걸린다.")
    with open(IDX, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
    print("OK archive_index.json — mails %d (inbox %d / sent %d), 신규 %d, 태그추가 %d"
          % (len(mails), len(inbox), len(sent), added, updated))


if __name__ == "__main__":
    main()
