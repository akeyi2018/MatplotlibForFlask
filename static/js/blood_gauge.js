
function drawBloodGauge(curHigh, curLow) {
    const gaugeWidth = 400;
    const gaugeHeight = 30;

    const gaugeContainer = document.getElementById('gauge-blood');
    gaugeContainer.innerHTML = '';

    // ゲージの表示
    const minBlood = 60;
    const maxBlood = 160;

    const gauge = document.createElement('div');
    gauge.style.width = gaugeWidth + 'px';
    gauge.style.height = gaugeHeight + 'px';
    gauge.style.position = 'relative'; // 相対位置に変更
    gaugeContainer.appendChild(gauge);

    // 血圧によって背景色を変更
    // ゲージの背景色を設定するサブ関数
    function drawBackground(min, max, color) {
        const start = Math.max(minBlood, min);
        const end = Math.min(maxBlood, max);
        const width = ((end - start) / (maxBlood - minBlood)) * gaugeWidth;
        
        const backgroundPart = document.createElement('div');
        backgroundPart.style.width = width + 'px';
        backgroundPart.style.height = gaugeHeight + 'px';
        backgroundPart.style.backgroundColor = color;
        backgroundPart.style.position = 'absolute';
        backgroundPart.style.left = ((start - minBlood) / (maxBlood - minBlood)) * gaugeWidth + 'px';
        gauge.appendChild(backgroundPart);
    }

    // 背景色を設定する
    drawBackground(60, 75, '#47fe12');
    drawBackground(75, 125, '#FF69B4');
    drawBackground(125, 180, '#fe1229');

    const labelsContainer = document.createElement('div');
    labelsContainer.style.width = '100%';
    labelsContainer.style.textAlign = 'center';
    labelsContainer.style.position = 'absolute';
    labelsContainer.style.bottom = '-35px';
    labelsContainer.style.left = '0';
    gaugeContainer.appendChild(labelsContainer);

    // メインメモリとサブメモリの描画
    for (let i = minBlood; i <= maxBlood; i++) {
        const isMainTick = (i - minBlood) % 10 === 0;
        const tickHeight = isMainTick ? gaugeHeight : gaugeHeight / 2;
        const tick = document.createElement('div');
        tick.style.width = '1px';
        tick.style.height = tickHeight + 'px';
        tick.style.backgroundColor = '#ffff';
        tick.style.position = 'absolute';
        tick.style.left = ((i - minBlood) / (maxBlood - minBlood)) * gaugeWidth + 'px';
        gauge.appendChild(tick);

        if (isMainTick) {
            // ラベル
            const label = document.createElement('div');
            label.textContent = i;
            label.style.position = 'absolute';
            label.style.bottom = '10px';
            label.style.transform = 'translateX(-50%)';
            label.style.left = ((i - minBlood) / (maxBlood - minBlood)) * gaugeWidth + 'px';
            labelsContainer.appendChild(label);
        }
        
        if (i < maxBlood){
            //サブメモリ描画
            for (let j = 1; j <= 1; j++) {
                const subTick = document.createElement('div');
                subTick.style.width = '1px';
                subTick.style.height = gaugeHeight / 2 + 'px';
                subTick.style.backgroundColor = '#fff';
                subTick.style.position = 'absolute';
                subTick.style.left = ((i - minBlood + j * 0.2) / (maxBlood - minBlood)) * gaugeWidth + 'px';
                gauge.appendChild(subTick);
            }
        }
    }

    function drawVerticalBars() {
        const verticalBar1 = document.createElement('div');
        // 横棒の開始位置（LOW）
        const low = ((curLow - minBlood) / (maxBlood - minBlood)) * gaugeWidth;
        // 横棒の長さの計算
        const w = ((curHigh - curLow) /  (maxBlood - minBlood)) * gaugeWidth;
        verticalBar1.style.width = w + 'px'; 
        verticalBar1.style.height = '30px'; // 縦棒の長さは20px
        verticalBar1.style.backgroundColor = `rgba(102, 16, 242, 0.6)`;
        verticalBar1.style.position = 'absolute';
        verticalBar1.style.left = low + 'px';
        verticalBar1.style.bottom = '0px';
        gauge.appendChild(verticalBar1);
      }
    drawVerticalBars();
}

// ページ読み込み時にゲージを描画
window.onload = drawBloodGauge(curHigh,curLow);