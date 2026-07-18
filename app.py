import streamlit as st
from Bio import SeqIO
import io
from alignment_logic import global_alignment, local_alignment, get_symbol

st.set_page_config(page_title="Bioinformatics Alignment", layout="centered")
st.title("Sequence Alignment Tool")

with st.sidebar:
    st.header("Parameters")
    match = st.number_input("Match Score", value=5)
    mismatch = st.number_input("Mismatch Score", value=-1)
    gap = st.number_input("Gap Penalty", value=-3)


input_method = st.radio("Choose input method:", ("Manual Text", "Upload FASTA File"))

def get_sequence(method, label, key):
    if method == "Manual Text":

        seq = st.text_input(f"enter {label}:",key=key)
        if seq:
            return seq.strip().upper()
        
    else:
        uploaded_file = st.file_uploader(f"Upload {label} file", type=["fasta", "fa"], key=key)
        if uploaded_file :
            
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))

            try:
                
                record = SeqIO.read(stringio, "fasta")
                return str(record.seq).upper()
            except Exception as e :
                st.error(f"Error reading FASTA file: {e}")
                return None 
    
    return ""

seq1 = get_sequence(input_method, "first sequence", "seq1")
seq2 = get_sequence(input_method, "second sequence", "seq2")

mode = st.radio("Alignment Mode", ("Global (Needleman-Wunsch)", "Local (Smith-Waterman)"))

if st.button("Run Alignment"):
    if not seq1 or not seq2:
        st.error("Please enter both sequences!")
    else:
        if "Global" in mode:
            align1, align2, score = global_alignment(seq1, seq2, match, mismatch, gap)
        else:
            align1, align2, score = local_alignment(seq1, seq2, match, mismatch, gap)
        
        st.success(f"Alignment Score: {score}")
        symbol = get_symbol(align1, align2)
        
        line_length = 80

        st.subheader("Alignment Result:")
        for i in range(0, len(align1), line_length):
            part1 = align1[i : i + line_length]
            part_sym = symbol[i : i + line_length]
            part2 = align2[i : i + line_length]
    
            st.code(f"{part1}\n{part_sym}\n{part2}", language="text")
            
























