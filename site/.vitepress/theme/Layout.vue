<!--
  Custom Layout — extends VitePress's default layout and fills the
  `home-hero-image` slot with NLPM's noun-verb map. Every other page
  inherits the default behavior; only the home page (layout: home) has
  the home hero, so the slot fill only renders there.
-->
<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import VocabMap from './components/VocabMap.vue'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #home-hero-image>
      <VocabMap />
    </template>
  </Layout>
</template>
