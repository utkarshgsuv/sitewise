"""S4 spike: pooled set_config must be transaction-local (no leak across pool checkouts).

Run: uv run python scripts/s4_pool_check.py
Exits 0 with a PASS report, non-zero otherwise.
"""
import os
import time

from sqlalchemy import create_engine, text

ORG = "11111111-1111-1111-1111-111111111111"


def main() -> None:
    url = os.environ["DATABASE_URL_POOLED"]
    t0 = time.time()
    e = create_engine(url, connect_args={"connect_timeout": 10}, pool_size=1, max_overflow=0)
    with e.connect() as c:
        t_conn = time.time() - t0
        with c.begin():
            got = c.execute(
                text("select set_config('app.org_id', :o, true)"), {"o": ORG}
            ).scalar()
            assert got == ORG, got
            cur = c.execute(text("select current_setting('app.org_id', true)")).scalar()
            assert cur == ORG, cur
            print(f"in-txn set_config visible: {cur}")
        # new transaction on same pooled connection: setting must be gone
        with c.begin():
            cur = c.execute(text("select current_setting('app.org_id', true)")).scalar()
            assert cur in (None, ""), f"LEAKED across txn: {cur!r}"
            print("post-commit setting cleared (no leak across txns)")
    # fresh checkout: definitely no leak
    with e.connect() as c2:
        cur = c2.execute(text("select current_setting('app.org_id', true)")).scalar()
        assert cur in (None, ""), f"LEAKED across connections: {cur!r}"
        print("fresh checkout clean (no leak across pooled connections)")
    print(f"cold connect+query: {t_conn:.1f}s")
    print("S4 set_config check: PASS")


if __name__ == "__main__":
    main()
