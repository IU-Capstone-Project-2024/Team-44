from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import User


class TestSummaryView(APITestCase):
    def test_post_method(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.is_active = True
        user.save()

        self.client.force_login(user=user)

        data = {'query': 'The exploration of Mars has been a long-standing goal of space agencies around the world. With its similarities to Earth, Mars has often been seen as a potential target for future human missions. However, before humans can set foot on the Red Planet, robotic missions are necessary to gather data and pave the way for human exploration. NASAs Perseverance Rover is the latest in a long line of Mars missions. Launched on July 30, 2020, the rover made its dramatic landing in the Jezero Crater on Feb. 18, 2021. The landing site was carefully chosen for its potential to host signs of ancient microbial life. Jezero Crater is believed to have once been a lake, and the rover will search for evidence of past life in the sediments left behind. The Perseverance Rover is equipped with a suite of advanced scientific instruments. These include a drill to collect samples of Martian rock and soil, a camera system to capture high-resolution images, and a miniature helicopter named Ingenuity to test powered flight on Mars. The rover will also test technologies to produce oxygen from the Martian atmosphere, a key step towards future human missions. The mission is expected to last at least one Martian year, or about 687 Earth days. During this time, the rover will traverse the Martian surface, collect and analyze samples, and send data back to Earth. The data gathered by Perseverance will not only advance our understanding of Mars, but also help pave the way for future human missions to the Red Planet.'}
        response = self.client.post("/summary/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestQuizView(APITestCase):
    def test_post_method(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.is_active = True
        user.save()

        self.client.force_login(user=user)

        data = {
            'text': 'Encoder: The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position- wise fully connected feed-forward network. We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1]. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512. Decoder: The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack. Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.'}
        response = self.client.post("/quiz/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
