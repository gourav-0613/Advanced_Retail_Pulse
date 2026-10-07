import os
import base64
import streamlit as st


def _flat(html: str) -> str:
    """Collapse multi-line / indented HTML into one line.

    st.markdown() treats any line indented by 4+ spaces as a CODE BLOCK, which
    made the page header render as raw text. Stripping every line avoids that.
    """
    return "".join(line.strip() for line in html.splitlines())


@st.cache_data
def icon(name: str) -> str:
    """Read SVG icon file, replace #60A5FA with currentColor, set width/height to 100%."""
    file_path = f"assets/icons/icon-{name}.svg"
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    svg_content = svg_content.replace('stroke="#60A5FA"', 'stroke="currentColor"')
    svg_content = svg_content.replace("viewBox=", 'width="100%" height="100%" viewBox=')
    return svg_content


def sidebar_brand():
    """Render top sidebar brand wordmark logo using st.logo with fallback."""
    wordmark_path = "assets/retailpulse-wordmark.svg"
    icon_path = "assets/retailpulse-logo.png"

    try:
        if hasattr(st, "logo"):
            st.logo(wordmark_path, icon_image=icon_path, size="large")
        else:
            st.sidebar.image(wordmark_path, use_container_width=True)
    except Exception:
        if os.path.exists(wordmark_path):
            st.sidebar.image(wordmark_path, use_container_width=True)
        else:
            st.sidebar.markdown("## Retail Pulse")


def page_header(icon_name: str, title: str, subtitle: str = ""):
    """Render page header with responsive inline SVG icon tile and h1 title."""
    svg_markup = icon(icon_name)
    sub_html = (
        f'<p class="rp-sub" style="margin-top:6px;margin-bottom:0;color:#9CA3AF;font-size:1.05rem;">{subtitle}</p>'
        if subtitle
        else ""
    )

    header_html = f"""
    <div class="rp-header" style="display:flex; flex-direction:column; gap:0.4rem; margin-bottom:1.5rem; padding-top:0.5rem;">
        <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
            <div class="rp-header-icon" style="
                width: clamp(42px, 6vw, 56px);
                height: clamp(42px, 6vw, 56px);
                min-width: clamp(42px, 6vw, 56px);
                background: linear-gradient(135deg, rgba(30,58,138,0.4), rgba(59,130,246,0.15));
                border: 1px solid rgba(96,165,250,0.35);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #60A5FA;
            ">
                <div style="width:55%; height:55%; display:flex; align-items:center; justify-content:center;">
                    {svg_markup}
                </div>
            </div>
            <h1 style="
                font-size: clamp(1.45rem, 1rem + 2vw, 2.4rem);
                font-weight: 700;
                color: #FFFFFF;
                margin: 0;
                line-height: 1.25;
                word-break: break-word;
            ">{title}</h1>
        </div>
        {sub_html}
    </div>
    """
    st.markdown(_flat(header_html), unsafe_allow_html=True)


def feature_cards(items: list):
    """Render grid feature cards."""
    cards_html = [
        '<div class="rp-cards" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap:1.25rem; margin-bottom:1.5rem;">'
    ]

    for item in items:
        icon_name = item.get("icon", "chart")
        title = item.get("title", "")
        desc = item.get("desc", item.get("description", ""))
        bullets = item.get("bullets", [])

        svg_markup = icon(icon_name)

        content_html = ""
        if desc:
            content_html += f'<p style="margin:0; font-size:0.92rem; color:#9CA3AF; line-height:1.5;">{desc}</p>'
        if bullets:
            bullet_items = "".join(
                [f'<li style="margin-bottom:0.35rem; color:#D1D5DB; font-size:0.9rem;">{b}</li>' for b in bullets]
            )
            content_html += f'<ul style="margin:0; padding-left:1.1rem; list-style-type:disc;">{bullet_items}</ul>'

        card_item = f"""
        <div class="rp-card" style="
            background: linear-gradient(135deg, #161B22 0%, #1b2432 100%);
            border: 1px solid #293548;
            border-radius: 18px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
            transition: transform 0.25s ease, border-color 0.25s ease;
        ">
            <div class="rp-card-icon" style="
                width: 44px;
                height: 44px;
                min-width: 44px;
                background: rgba(59, 130, 246, 0.12);
                border: 1px solid rgba(96, 165, 250, 0.25);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #60A5FA;
            ">
                <div style="width:55%; height:55%; display:flex; align-items:center; justify-content:center;">
                    {svg_markup}
                </div>
            </div>
            <h3 style="margin:0; font-size:1.15rem; font-weight:600; color:#F3F4F6;">{title}</h3>
            {content_html}
        </div>
        """
        cards_html.append(card_item)

    cards_html.append("</div>")
    st.markdown(_flat("".join(cards_html)), unsafe_allow_html=True)


def hero_image(path: str = "assets/hero.svg"):
    """Embed SVG image centered with responsive max-width."""
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        data = f.read()
    b64_data = base64.b64encode(data).decode("utf-8")

    html = f"""
    <div class="rp-hero" style="width:100%; display:flex; justify-content:center; margin:1rem 0 1.5rem 0;">
        <img src="data:image/svg+xml;base64,{b64_data}" style="width:100%; height:auto; max-width:1000px; border-radius:14px;" alt="Retail Pulse Banner" />
    </div>
    """
    st.markdown(_flat(html), unsafe_allow_html=True)


def style_fig(fig, height: int = 450, margin_r: int = 20):
    """Style Plotly figures with dark theme, horizontal bottom legend, automargins, and correct titles."""
    has_title = False
    if hasattr(fig.layout, "title") and fig.layout.title and getattr(fig.layout.title, "text", None):
        if str(fig.layout.title.text).strip():
            has_title = True

    has_legend = False
    if hasattr(fig, "data"):
        for trace in fig.data:
            if getattr(trace, "showlegend", True) and getattr(trace, "name", None):
                has_legend = True
                break

    t_margin = 60 if has_title else 20
    b_margin = 80 if has_legend else 20

    layout_update = dict(
        template="plotly_dark",
        autosize=True,
        height=height,
        font=dict(size=13),
        margin=dict(l=10, r=margin_r, t=t_margin, b=b_margin),
    )

    if has_legend:
        layout_update["legend"] = dict(
            orientation="h",
            y=-0.18,
            xanchor="center",
            x=0.5,
            title=dict(text="")
        )

    if has_title:
        layout_update["title_x"] = 0.02
        layout_update["title_font"] = dict(size=16)

    fig.update_layout(**layout_update)
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig
