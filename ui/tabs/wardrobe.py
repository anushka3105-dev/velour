# ─────────────────────────────────────────────
# ui/tabs/wardrobe.py — Wardrobe Manager tab
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
from database.db import load_wardrobe, add_wardrobe_item, delete_wardrobe_item
from config import OPTIONS, CATEGORY_ICONS


def render_wardrobe_tab(user: dict):
    """Render the wardrobe manager tab."""
    st.markdown('<div class="section-label">My Wardrobe</div>', unsafe_allow_html=True)

    col_add, col_list = st.columns([1, 2])

    with col_add:
        _render_add_item_form(user)

    with col_list:
        _render_wardrobe_list(user)


# ── Private helpers ───────────────────────────

def _render_add_item_form(user: dict):
    st.markdown("**Add New Item**")

    item_name     = st.text_input("Item Name",  placeholder="e.g. Black Blazer")
    item_category = st.selectbox("Category",    OPTIONS["category"])
    item_color    = st.text_input("Colour",     placeholder="e.g. Camel")
    item_occasion = st.selectbox("Best For",    OPTIONS["occasion_wear"])
    item_season   = st.selectbox("Season",      OPTIONS["season"])

    if st.button("＋  Add to Wardrobe"):
        if not item_name.strip():
            st.warning("Enter an item name.")
            return

        ok = add_wardrobe_item(user["id"], {
            "item_name": item_name.strip(),
            "category":  item_category,
            "color":     item_color or "—",
            "occasion":  item_occasion,
            "season":    item_season,
            "icon":      CATEGORY_ICONS.get(item_category, "👗"),
        })

        if ok:
            st.success(f"'{item_name}' added!")
            st.rerun()
        else:
            st.error("Could not add item. Check Supabase connection.")


def _render_wardrobe_list(user: dict):
    wardrobe = load_wardrobe(user["id"])

    if not wardrobe:
        st.markdown("""
        <div style='text-align:center; padding:3rem; color:#C4874A;'>
            <div style='font-size:3rem;'>👗</div>
            <div style='font-family:"Cormorant Garamond",serif; font-size:1.3rem;'>Your wardrobe is empty</div>
            <div style='font-size:0.8rem; margin-top:0.4rem; color:#A0622A;'>Add your first item using the form on the left</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Summary metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items",  len(wardrobe))
    c2.metric("Categories",   len(set(i["category"] for i in wardrobe)))
    c3.metric("Outfits Est.", len(wardrobe) * 2)

    st.markdown("<br>", unsafe_allow_html=True)

    # Category filter
    categories   = ["All"] + sorted(set(i["category"] for i in wardrobe))
    filter_cat   = st.selectbox("Filter by Category", categories)
    items_shown  = wardrobe if filter_cat == "All" else [i for i in wardrobe if i["category"] == filter_cat]

    # Item rows
    for item in items_shown:
        col_item, col_del = st.columns([5, 1])
        with col_item:
            st.markdown(f"""
            <div class="wardrobe-item">
                <div class="wardrobe-icon">{item.get('icon', '👗')}</div>
                <div>
                    <strong>{item['item_name']}</strong><br>
                    <span style="color:#A0622A; font-size:0.75rem;">
                        {item['category']} · {item.get('color','—')} · {item['occasion']} · {item['season']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_del:
            if st.button("✕", key=f"del_{item['id']}"):
                delete_wardrobe_item(item["id"])
                st.rerun()

    # Export
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥  Export Wardrobe as CSV"):
        df = pd.DataFrame(wardrobe)
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            f"wardrobe_{user['username']}.csv",
            "text/csv",
        )
