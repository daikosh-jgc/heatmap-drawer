import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# メインクラス
class HeatmapDrawer(object):
    def __init__(self):
        pass

    def download_link(self, object_to_download, download_filename, download_link_text):
        """ダウンロードリンクの生成"""
        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
        
    def open(self):
        """コンテンツページの表示"""

        # タイトルの表示
        st.title("Heatmap Drawer")

        # ファイルアップローダーを表示
        uploaded_file = st.sidebar.file_uploader("Upload a csv file / csvファイルをアップロード")
        
        # パラメータ設定を表示
        parameters_expander = st.sidebar.expander("Parameters / パラメータ", expanded=True) 
        dpi = parameters_expander.number_input("dpi", min_value=100, max_value=600)
        vmax = parameters_expander.number_input("Max. Value / 最大値", value=1.00)
        vmin = parameters_expander.number_input("Min. Value / 最小値", value=0.00)
        center = parameters_expander.number_input("Center Value / 中心値", value=0.50)
        cmap = parameters_expander.selectbox("Color Map / カラーマップ", [
            'viridis', 'plasma', 'inferno', 'magma',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper',
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c',
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])
        parameters_expander.markdown("[Color Map一覧](https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html)")
        
        # ラベル設定を表示
        labels_expander = st.sidebar.expander("Labels / ラベル", expanded=False)
        xlabel = labels_expander.text_input("x-axis / x軸")
        ylabel = labels_expander.text_input("y-axis / y軸")
        xticklabels= labels_expander.radio("x-axis ticks/ x軸目盛り", [False, True])
        yticklabels= labels_expander.radio("y-axis ticks/ y軸目盛り", [False, True])

        # Drawボタンが押された場合
        is_draw_button = st.button("Draw")
        if uploaded_file is not None and is_draw_button:
            
            # アップロードファイルをインポート
            df_uploaded = pd.read_csv(uploaded_file, header=None)

            # ヒートマップを表示
            fig = plt.figure(figsize=(12, 12), dpi=dpi)
            sns.heatmap(
                df_uploaded,
                cmap=cmap,
                vmax=vmax,
                vmin=vmin,
                center=center,
                square=True,
                xticklabels=xticklabels,
                yticklabels=yticklabels
                )
            plt.xlabel(xlabel, fontsize=20)
            plt.ylabel(str(ylabel))
            with st.expander("Heatmap", expanded=True):
                st.pyplot(fig)
            with st.expander("Uploaded Data", expanded=False):
                st.dataframe(df_uploaded)

        # Drawボタンが押されていない場合
        else:
            # 警告を表示
            st.warning("Please upload a csv file and press Draw button.")


# メイン関数
def main():
    # インスタンスの生成
    heatmap_drawer = HeatmapDrawer()
    heatmap_drawer.open()


if __name__ == "__main__":
    main()
