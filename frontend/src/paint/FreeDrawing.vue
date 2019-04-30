<template>
  <div>
    <div ref="container">
      <canvas
        :width="width/2"
        :height="height/2"
        ref="canvas">
      </canvas>
    </div>
  </div>
</template>

<script>
import Konva from 'konva';

export default {
  name: 'FreeDrawing',
  props: {
    mode: {
      type: String,
      default: ''
    },
    backgroundImage: {
      type: String,
      default: ''
    },
    brushColor: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    width: window.innerWidth,
    height: window.innerHeight,
    stage: null,
    drawingLayer: null,
    drawingScope: null,
    canvas: null,
    context: null,
    isPaint: false,
    lastPointerPosition: {},
    localPos: {
      x: 0,
      y: 0
    },
    pos: null,
    undoDataStack: [], // 戻る配列
    redoDataStack: [], // 進む配列
    imageObj: null,
    backgroundImageLayer: null,
    backgroundImageScope: null
  }),
  mounted: function() {
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext('2d');

    var container = this.$refs.container;
    this.stage = new Konva.Stage({
      container,
      width: this.width,
      height: this.height
    });

    this.drawingLayer = new Konva.Layer();
    this.stage.add(this.drawingLayer);

    this.drawingScope = new Konva.Image({
      image: this.canvas,
      x: this.width / 4
      // stroke: 'black',
    });
    this.drawingLayer.add(this.drawingScope);

    this.imageObj = new Image();
    this.imageObj.addEventListener('load', this.imageOnload);
    this.imageObj.src = this.backgroundImage;
    this.stage.draw();

    this.context.strokeStyle = this.brushColor;
    this.context.lineJoin = 'round';
    this.context.lineWidth = 5;

    // イベント追加
    this.drawingScope.on('mousedown touchstart', this.mousedown);
    this.stage.addEventListener('mouseup', this.mouseup);
    this.stage.addEventListener('touchend', this.mouseup);
    this.stage.addEventListener('mousemove', this.mousemove);
    this.stage.addEventListener('touchmove', this.mousemove);
  },
  methods: {
    /**  描画開始
     *   マウスダウン時の座標を取得しておく
     */
    mousedown: function() {
      // 戻る配列に描画前のキャンバスイメージを保存しておく
      this.undoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));

      this.isPaint = true;
      this.lastPointerPosition = this.stage.getPointerPosition();
    },
    /** 描画終了 */
    mouseup: function() {
      this.isPaint = false;

      // 直線モードの時はマウスを話したときに描画されるようにする
      if (this.isTargetMode('line')) {
        this.drawToCanvas();
      }
    },
    mousemove: function() {
      if (!this.isPaint) {
        return;
      }
      // ペンモード時
      if (this.isTargetMode('brush') || this.isTargetMode('line')) {
        this.context.globalCompositeOperation = 'source-over';
      }
      // 消しゴムモード時
      if (this.isTargetMode('eraser')) {
        this.context.globalCompositeOperation = 'destination-out';
      }
      this.context.beginPath();

      this.localPos.x = this.lastPointerPosition.x - this.drawingScope.x();
      this.localPos.y = this.lastPointerPosition.y - this.drawingScope.y();

      // 開始座標を指定する
      this.context.moveTo(this.localPos.x, this.localPos.y);

      // ペンモード
      if (this.isTargetMode('brush')) {
        this.drawToCanvas();
      }
    },
    /** リセットボタン押下時、キャンバスをクリアするメソッド */
    onClearCanvas: function() {
      this.undoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));
      this.context.globalCompositeOperation = 'destination-out';
      this.context.fillRect(0, 0, this.width, this.height);
      this.drawingLayer.draw();

      this.$emit('on-reset');
    },
    getImageData: function() {
      return this.canvas.toDataURL('image/png');
    },
    imageOnload: function() {
      // 背景レイヤ
      this.backgroundImageLayer = new Konva.Layer();

      // 背景イメージ
      this.backgroundImageScope = new Konva.Image({
        image: this.imageObj,
        x: this.width / 4 - 1,
        width: this.canvas.width,
        height: this.canvas.height
      });
      // 背景レイヤに背景メージを追加
      this.backgroundImageLayer.add(this.backgroundImageScope);
      this.stage.add(this.backgroundImageLayer);

      // moveToBottomで画像を最背面に移動（これをしないと、ペンの描画が画像の下に潜ってしまう）
      this.backgroundImageLayer.moveToBottom();
    },
    drawToCanvas: function() {
      this.pos = this.stage.getPointerPosition();
      this.localPos.x = this.pos.x - this.drawingScope.x();
      this.localPos.y = this.pos.y - this.drawingScope.y();
      this.context.lineTo(this.localPos.x, this.localPos.y);

      this.context.closePath();
      this.context.stroke();

      this.lastPointerPosition = this.pos;
      this.drawingLayer.draw();
    },
    // 現在のモードが指定されたモードと一致するかどうか
    isTargetMode: function(targetMode) {
      return this.mode === targetMode;
    },
    // 戻る
    undo: function() {
      // 元に戻す配列に何もない場合は何もしない
      if (this.undoDataStack.length <= 0) {
        return;
      }

      // 進む配列に、戻る前のキャンバスイメージを保存しておく
      this.redoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));

      // キャンバスを1つ前の状態に戻す
      this.context.putImageData(this.undoDataStack.pop(), 0, 0);
      this.drawingLayer.draw();
    },
    // 進む
    redo: function() {
      // 進む配列に何もない場合は何もしない
      if (this.redoDataStack.length <= 0) {
        return;
      }

      // 戻る配列に、進む前のキャンバスイメージを保存しておく
      this.undoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));

      // キャンバスの状態を進める
      this.context.putImageData(this.redoDataStack.pop(), 0, 0);
      this.drawingLayer.draw();
    }
  },
  watch: {
    // ペンの色変更時
    brushColor: function() {
      this.context.strokeStyle = this.brushColor;
    }
  }
}
</script>
