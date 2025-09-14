import os
import torch
from typing import Optional, Tuple, Union
from transformers import CodeGenForCausalLM
from transformers.modeling_outputs import CausalLMOutputWithPast

class CodeGenPrefixCausalLM(CodeGenForCausalLM):
    def __init__(self, config):
        super().__init__(config)

        self.n_embed_per_head = config.n_embd // config.n_head
        if config.n_vul_token != 0:
            self.vul_params = torch.nn.ParameterList()
            for _ in range(len(config.vul_types)):
                for _ in range(config.n_layer):
                    for _ in range(2):
                        param_size = (config.n_head, config.n_vul_token, self.n_embed_per_head)
                        param = torch.nn.Parameter(torch.zeros(param_size, requires_grad=True))
                        # param = torch.nn.Parameter(torch.normal(mean=0.0, std=self.config.initializer_range, size=param_size, requires_grad=True))
                        self.vul_params.append(param)
        self.prefix_params = torch.nn.ParameterList()
        for _ in range(config.n_control):
            for _ in range(config.n_layer):
                for _ in range(2):
                    param_size = (config.n_head, config.n_prefix_token-config.n_vul_token, self.n_embed_per_head)
                    param = torch.nn.Parameter(torch.zeros(param_size, requires_grad=True))
                    # param = torch.nn.Parameter(torch.normal(mean=0.0, std=self.config.initializer_range, size=param_size, requires_grad=True))
                    self.prefix_params.append(param)
        self.dropout = torch.nn.Dropout(config.prefix_dropout)

    def get_past_from_prefix(self, vul_ids, control_ids):
        past = list()
        for i in range(self.config.n_layer):
            past.append(list())
            key_stack, val_stack = [], []
            for vul_id, control_id in zip(vul_ids, control_ids):
                control_key_idx = control_id * self.config.n_layer * 2 + i * 2
                control_val_idx = control_key_idx + 1
                control_key = self.dropout(self.prefix_params[control_key_idx])
                control_val = self.dropout(self.prefix_params[control_val_idx])

                if vul_id != -1 and self.config.n_vul_token != 0:
                    vul_key_idx = vul_id * self.config.n_layer * 2 + i * 2
                    vul_val_idx = vul_key_idx + 1
                    vul_key = self.dropout(self.vul_params[vul_key_idx])
                    vul_val = self.dropout(self.vul_params[vul_val_idx])
                    key = torch.cat((vul_key, control_key), dim=-2)
                    val = torch.cat((vul_val, control_val), dim=-2)
                else:
                    key, val = control_key, control_val

                key_stack.append(key)
                val_stack.append(val)
            past[i].append(torch.stack(key_stack))
            past[i].append(torch.stack(val_stack))
        return past

    def prepare_inputs_for_generation(self, input_ids, past=None, **kwargs):
        token_type_ids = kwargs.get("token_type_ids", None)
        if past:
            input_ids = input_ids[:, -1].unsqueeze(-1)
            if token_type_ids is not None:
                token_type_ids = token_type_ids[:, -1].unsqueeze(-1)
        else:
            vul_ids = [kwargs['vul_id']] * input_ids.shape[0]
            control_ids = [kwargs['control_id']] * input_ids.shape[0]
            past = self.get_past_from_prefix(vul_ids, control_ids)

        return {
            "input_ids": input_ids,
            "past_key_values": past,
            "use_cache": kwargs.get("use_cache"),
            "position_ids": None,
            "attention_mask": None,
            "token_type_ids": token_type_ids,
        }

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Tuple[Tuple[torch.Tensor]]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        token_type_ids: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        control_id = None, # placeholder for passing checks of huggingface, actually unused in this function
        vul_id = None, # placeholder for passing checks of huggingface, actually unused in this function
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        return super().forward(
            input_ids=input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict
        )

class Classifier(torch.nn.Module):
    def __init__(self, n_embed):
        super().__init__()
        self.n_embed = n_embed
        self.linear = torch.nn.Linear(self.n_embed, 2)

    def forward(self, inputs):
        return self.linear(inputs)

    def save_pretrained(self, path):
        torch.save(self.state_dict(), os.path.join(path, 'pytorch_model.bin'))

    def load(self, path):
        self.load_state_dict(torch.load(os.path.join(path, 'pytorch_model.bin')))