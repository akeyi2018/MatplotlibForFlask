function drawGauge(curWeight, gWeight) {
    const gaugeWidth = 400;
    const gaugeHeight = 30;

    const gaugeContainer = document.getElementById('gauge-container');
    gaugeContainer.innerHTML = '';

    const minWeight = gWeight;
    const maxWeight = 80;

    const gauge = document.createElement('div');
    gauge.style.width = gaugeWidth + 'px';
    gauge.style.height = gaugeHeight + 'px';
    gauge.style.position = 'relative'; // 相対位置に変更
    gaugeContainer.appendChild(gauge);

    // 体重によって背景色を変更
    // ゲージの背景色を設定するサブ関数
    function drawBackground(min, max, color) {
        const start = Math.max(minWeight, min);
        const end = Math.min(maxWeight, max);
        const width = ((end - start) / (maxWeight - minWeight)) * gaugeWidth;
        
        const backgroundPart = document.createElement('div');
        backgroundPart.style.width = width + 'px';
        backgroundPart.style.height = gaugeHeight + 'px';
        backgroundPart.style.backgroundColor = color;
        backgroundPart.style.position = 'absolute';
        backgroundPart.style.left = ((start - minWeight) / (maxWeight - minWeight)) * gaugeWidth + 'px';
        gauge.appendChild(backgroundPart);
    }

    // 背景色を設定する
    drawBackground(60, 68, '#47fe12');
    drawBackground(68, 81, '#e1e10d');
    drawBackground(81, 90, '#fe1229');

    const labelsContainer = document.createElement('div');
    labelsContainer.style.width = '100%';
    labelsContainer.style.textAlign = 'center';
    labelsContainer.style.position = 'absolute';
    labelsContainer.style.bottom = '-35px';
    labelsContainer.style.left = '0';
    gaugeContainer.appendChild(labelsContainer);

    // メインメモリとサブメモリの描画
    for (let i = minWeight; i <= maxWeight; i++) {
        const isMainTick = (i - minWeight) % 1 === 0;
        const tickHeight = isMainTick ? gaugeHeight : gaugeHeight / 2;
        const tick = document.createElement('div');
        tick.style.width = '1px';
        tick.style.height = tickHeight + 'px';
        tick.style.backgroundColor = '#ffff';
        tick.style.position = 'absolute';
        tick.style.left = ((i - minWeight) / (maxWeight - minWeight)) * gaugeWidth + 'px';
        gauge.appendChild(tick);

        if (isMainTick) {
            // ラベル
            const label = document.createElement('div');
            label.textContent = i;
            label.style.position = 'absolute';
            label.style.bottom = '10px';
            label.style.transform = 'translateX(-50%)';
            label.style.left = ((i - minWeight) / (maxWeight - minWeight)) * gaugeWidth + 'px';
            labelsContainer.appendChild(label);
        }
        
        if (i < maxWeight){
            //サブメモリ描画
            for (let j = 1; j <= 9; j++) {
                const subTick = document.createElement('div');
                subTick.style.width = '1px';
                subTick.style.height = gaugeHeight / 2 + 'px';
                subTick.style.backgroundColor = '#fff';
                subTick.style.position = 'absolute';
                subTick.style.left = ((i - minWeight + j * 0.1) / (maxWeight - minWeight)) * gaugeWidth + 'px';
                gauge.appendChild(subTick);
            }
        }
    }

    function drawVerticalBars() {
        const verticalBar1 = document.createElement('div');
        // 横棒の長さの計算 
        const w = gaugeWidth - ((curWeight - minWeight) / (maxWeight - minWeight)) * gaugeWidth;
        verticalBar1.style.width = w + 'px'; 
        verticalBar1.style.height = '30px'; // 縦棒の長さは20px
        verticalBar1.style.backgroundColor = `rgba(102, 16, 242, 0.6)`;
        verticalBar1.style.position = 'absolute';
        verticalBar1.style.left = (gaugeWidth - w) + 'px';
        verticalBar1.style.bottom = '0px';
        gauge.appendChild(verticalBar1);
      }
    drawVerticalBars();
}

function currentWeight(gauge, currentWeight, minWeight, maxWeight, gaugeWidth, gaugeHeight){
    // 逆三角形を描画する
    const triangle = document.createElement('div');
    triangle.style.borderLeft = '10px solid transparent';
    triangle.style.borderRight = '10px solid transparent';
    triangle.style.borderTop = '15px solid yellow';
    triangle.style.position = 'absolute';
    triangle.style.left = ((currentWeight - minWeight) / (maxWeight - minWeight)) * gaugeWidth - 10 + 'px';
    triangle.style.bottom = gaugeHeight + 'px';
    gauge.appendChild(triangle);

}

function goalWeight(gauge, currentWeight, minWeight, maxWeight, gaugeWidth, gaugeHeight){
    // 縦棒を描画する
    const currentWeightTick = document.createElement('div');
    currentWeightTick.style.width = '2px'; // 縦棒の幅は2px
    currentWeightTick.style.height = '40px'; // 縦棒の長さは20px
    currentWeightTick.style.backgroundColor = 'blue';

    currentWeightTick.style.position = 'absolute';
    currentWeightTick.style.left = ((currentWeight - minWeight) / (maxWeight - minWeight)) * gaugeWidth + 'px';
    currentWeightTick.style.bottom = 0;
    gauge.appendChild(currentWeightTick);

}

// ページ読み込み時にゲージを描画
window.onload = drawGauge(curWeight,gWeight);