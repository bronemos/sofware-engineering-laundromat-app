<template>
  <transition name="preview">
        <div class="overlay">
            <div class="media font-theme text-left">
                <div class="media-body post-theme p-5">
                    <h5 class="lead">
                        <b-avatar class="mb-2"></b-avatar>
                        <strong>
                        {{ this.$auth.user.username }}
                        </strong>
                        <span class="three-dots"><strong>...</strong></span>
                    </h5>

                    <hr class="mt-2 post-separator-theme" />

                    <div class="post-image">
                        <img :src="imgUrl">
                    </div>   
                    <hr class="mt-2 post-separator-theme" />
                    <span>
                    <button
                        @click="allowPost(true)"
                        class="btn btn-purple btn-fill mt-2 text-align btn-post"
                        >
                        Post
                    </button>
                    <button
                        @click="allowPost(false)"
                        class="btn btn-purple btn-fill mt-2 text-align btn-post"
                        >
                        Discard
                    </button>
                    </span>
                </div>
            </div>
        </div>
  </transition>
</template>


<script>

export default {
    name: "ImagePreview",
    props: {
        post: Object
    },
    methods: {
        allowPost(allowPost) {
            this.$emit("post", allowPost);
        }
    },
    computed: {
        imgUrl() {
            return URL.createObjectURL(this.post.image);
        }
    }
}

</script>