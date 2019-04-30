<template>
    <div>
        <div class="md-layout md-gutter" style="margin-left: 340px">
          <div class="md-layout-item">
            <md-field style="float: left">
              <label for="mode">モード</label>
              <md-select v-model="mode" name="mode" id="mode">
                <md-option value="brush">ペン</md-option>
                <md-option value="eraser">消しゴム</md-option>
                <md-option value="line">直線</md-option>
              </md-select>
            </md-field>

            <md-field style="float: left">
              <label for="brushColor">ペンの色</label>
              <md-input type="color" v-model="brushColor" />
            </md-field>

            <md-field style="float: left; margin-top: -8px">
              <md-button
                class="md-dense md-raised md-primary"
                @click="onUndo"
              >
                戻る
              </md-button>
            </md-field>

            <md-field style="float: left; margin-top: -8px">
              <md-button
                class="md-dense md-raised md-primary"
                @click="onRedo"
              >
                進む
              </md-button>
            </md-field>

            <md-field style="float: left; margin-top: -8px">
              <md-button
                class="md-dense md-raised md-primary"
                @click="onClearCanvas"
              >
                  リセット
              </md-button>
            </md-field>

            <md-field style="float: left; margin-top: -8px">
              <md-button
                class="md-dense md-raised md-primary"
                @click="onSaveImageFile"
              >
                  保存
              </md-button>
            </md-field>
          </div>
        </div>
        <!-- <FreeDrawingTest
            :mode="mode"
            ref="FreeDrawingTest"
        /> -->
        <FreeDrawing
            :mode="mode"
            :backgroundImage="baseImage"
            :brushColor="brushColor"
            @on-reset="onReset"
            ref="FreeDrawing"
        />
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import FreeDrawing from './FreeDrawing.vue';
// import FreeDrawingTest from './FreeDrawingTest.vue';

export default {
  name: 'CallCanvas',
  components: {
    FreeDrawing
    // FreeDrawingTest
  },
  data: () => ({
    mode: 'brush',
    brushColor: '#FFFFFF',
    defaultMode: 'brush',
    defaultBrushColor: '#FFFFFF'
  }),
  methods: {
    ...mapActions(['SAVE_IMAGE_FILE']),
    onClearCanvas: function() {
      // this.$refs.FreeDrawingTest.onClearCanvas();
      this.$refs.FreeDrawing.onClearCanvas();
    },
    onSaveImageFile: function() {
      var base64ImageData = this.$refs.FreeDrawing.getImageData();
      if (base64ImageData) {
        const request = {
          file: base64ImageData
        }
        this.SAVE_IMAGE_FILE(request).then(function(res) {
          console.log(res);
        });
      }
    },
    onReset: function() {
      this.mode = this.defaultMode;
      this.brushColor = this.defaultBrushColor;
    },
    onUndo: function() {
      this.$refs.FreeDrawing.undo();
    },
    onRedo: function() {
      this.$refs.FreeDrawing.redo();
    }
  },
  computed: {
    baseImage: function() {
      return require('../assets/fotome_logo.png');
    }
  }
}
</script>

<style lang="scss" scoped>
  .md-field {
    max-width: 110px;
  }
</style>
