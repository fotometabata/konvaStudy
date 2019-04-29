<template>
  <div>
    <img src="../assets/logo.png" alt="">
    <div ref="container">
      <canvas
        :width="width / 2"
        :height="height / 2"
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
    undoDataStack: [],
    redoDataStack: [],
    imageObj: null
  }),
  mounted: function() {
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext('2d');

    var container = this.$refs.container;
    this.stage = new Konva.Stage({
      container,
      width: this.width,
      height: this.height / 1.8
    });

    this.drawingLayer = new Konva.Layer();
    this.stage.add(this.drawingLayer);

    // イメージの指定がない場合は白紙のキャンバスを表示する
    if (!this.backgroundImage) {
      this.drawingScope = new Konva.Image({
        image: this.canvas,
        x: this.stage.width() / 4,
        y: 5,
        stroke: 'green',
        shadowBlur: 5
      });
      this.drawingLayer.add(this.drawingScope);
    }
    this.stage.draw();

    this.context.strokeStyle = '#df4b26';
    this.context.lineJoin = 'round';
    this.context.lineWidth = 5;

    this.drawingScope.on('mousedown touchstart', this.mousedown);

    this.stage.addEventListener('mouseup', this.mouseup);
    this.stage.addEventListener('touchend', this.mouseup);

    this.stage.addEventListener('mousemove', this.mousemove);
    this.stage.addEventListener('touchmove', this.mousemove);

    this.beforeDraw();
  },
  methods: {
    mousedown: function() {
      this.isPaint = true;
      this.lastPointerPosition = this.stage.getPointerPosition();
    },
    mouseup: function() {
      this.isPaint = false;
    },
    mousemove: function() {
      if (!this.isPaint) {
        return;
      }

      if (this.mode === 'brush') {
        this.context.globalCompositeOperation = 'source-over';
      }
      if (this.mode === 'eraser') {
        this.context.globalCompositeOperation = 'destination-out';
      }
      this.context.beginPath();

      this.localPos.x = this.lastPointerPosition.x - this.drawingScope.x();
      this.localPos.y = this.lastPointerPosition.y - this.drawingScope.y();

      this.context.moveTo(this.localPos.x, this.localPos.y);
      this.pos = this.stage.getPointerPosition();
      this.localPos.x = this.pos.x - this.drawingScope.x();
      this.localPos.y = this.pos.y - this.drawingScope.y();

      this.context.lineTo(this.localPos.x, this.localPos.y);
      this.context.closePath();
      this.context.stroke();

      this.lastPointerPosition = this.pos;
      this.drawingLayer.draw();
    },
    beforeDraw: function() {
      // 元に戻す配列の先頭にcontextのImageDataを保持する
      this.undoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));
    },
    onClearCanvas: function() {
      this.undoDataStack.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));
      this.context.globalCompositeOperation = 'destination-out';
      this.context.fillRect(0, 0, this.width, this.height);
      this.drawingLayer.draw();
    },
    getImageData: function() {
      return this.canvas.toDataURL('image/png');
    }
  },
  watch: {
    mode: function() {
      console.log(this.mode);
    }
  }
}
</script>
